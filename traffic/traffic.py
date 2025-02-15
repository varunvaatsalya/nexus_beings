from ultralytics import YOLO
import cv2
import numpy as np
import easyocr  # Import EasyOCR
import os
import time

##############################################
# 1. INITIALIZE YOLO, EASYOCR & CONFIGURATION
##############################################

# Load the YOLO model (adjust model path as needed)
model = YOLO("yolov8n.pt")

# Initialize EasyOCR reader (for English)
reader = easyocr.Reader(['en'])

# Mapping from YOLO class names to our simplified categories
vehicle_classes = {
    "motorcycle": "2-wheeler",
    "bicycle": "2-wheeler",
    "car": "car",
    "truck": "large vehicle",
    "bus": "large vehicle",
    "ambulance": "emergency vehicle",   # if detected directly by YOLO
    "fire truck": "emergency vehicle"
}

# Time (in seconds) assigned per vehicle (excluding emergency vehicles)
time_assignment = {
    "2-wheeler": 3,    # 3 seconds for each two-wheeler
    "car": 5,          # 5 seconds for each car (small 4-wheeler)
    "large vehicle": 7 # 7 seconds for each heavy vehicle
}

# Directory to save emergency captures
save_dir = "emergency_captures"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

##############################################
# 2. LANE DETECTION FUNCTIONS (Classic CV)
##############################################

def region_selection(image):
    """Apply a mask to focus on the region of interest (the road)."""
    mask = np.zeros_like(image)
    ignore_mask_color = 255 if len(image.shape) == 2 else (255,) * image.shape[2]
    rows, cols = image.shape[:2]
    # Define a polygon for the road region (adjust as needed)
    vertices = np.array([[
        [cols * 0.1, rows * 0.95],
        [cols * 0.4, rows * 0.6],
        [cols * 0.6, rows * 0.6],
        [cols * 0.9, rows * 0.95]
    ]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    return cv2.bitwise_and(image, mask)

def hough_transform(image):
    """Detect lines in the image using Hough Transform."""
    return cv2.HoughLinesP(image, 1, np.pi/180, 20, minLineLength=20, maxLineGap=500)

def average_slope_intercept(lines):
    """Average out the detected lines to get one left and one right lane."""
    left, right = [], []
    left_weights, right_weights = [], []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue  # skip vertical lines
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            length = np.sqrt((y2 - y1)*2 + (x2 - x1)*2)
            if slope < 0:
                left.append((slope, intercept))
                left_weights.append(length)
            else:
                right.append((slope, intercept))
                right_weights.append(length)
    left_lane = np.dot(left_weights, left) / np.sum(left_weights) if left_weights else None
    right_lane = np.dot(right_weights, right) / np.sum(right_weights) if right_weights else None
    return left_lane, right_lane

def pixel_points(y1, y2, line):
    """Convert the slope and intercept into pixel points."""
    if line is None:
        return None
    slope, intercept = line
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, int(y1)), (x2, int(y2))

def lane_lines(image, lines):
    """Generate lane lines (pixel endpoints) from the detected lines."""
    left_lane, right_lane = average_slope_intercept(lines)
    y1 = image.shape[0]
    y2 = int(y1 * 0.6)
    return pixel_points(y1, y2, left_lane), pixel_points(y1, y2, right_lane)

def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=8):
    """Draw the lane lines onto the image."""
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            cv2.line(line_image, *line, color, thickness)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0)

##############################################
# 3. VEHICLE DETECTION & TRAFFIC MANAGEMENT
##############################################

def process_frame(frame):
    """
    Process a single frame:
      - Run lane detection.
      - Run YOLO detection to count and classify vehicles.
      - Use EasyOCR to identify emergency vehicles based on text.
      - Overlay lane lines, bounding boxes, and traffic info.
    Returns the annotated frame and a dictionary of vehicle counts.
    """
    # ----- Lane Detection -----
    lane_frame = frame.copy()
    grayscale = cv2.cvtColor(lane_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    region = region_selection(edges)
    lines = hough_transform(region)
    if lines is not None:
        lane_frame = draw_lane_lines(lane_frame, lane_lines(lane_frame, lines))
    
    # ----- Vehicle Detection using YOLO -----
    results = model(frame)[0]  # Run YOLO on the frame
    # Initialize counts for each category
    vehicle_counts = {"2-wheeler": 0, "car": 0, "large vehicle": 0, "emergency vehicle": 0}
    
    for det in results.boxes.data:
        # Get detection coordinates, confidence, and class index
        x1, y1, x2, y2, conf, cls = det.cpu().numpy()
        class_name = model.names[int(cls)]
        # Use our mapping if available
        category = vehicle_classes.get(class_name, None)
        
        # Convert coordinates to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        # Extract region of interest (ROI) from the frame
        roi = frame[y1:y2, x1:x2]
        
        # Use EasyOCR to detect emergency text if ROI is valid
        if roi.size > 0:
            ocr_results = reader.readtext(roi)
            # Concatenate all detected text and convert to uppercase for consistency
            detected_text = " ".join([res[1] for res in ocr_results]).upper()
            # Check for keywords indicating emergency vehicles
            if "AMBULANCE" in detected_text or "POLICE" in detected_text:
                category = "emergency vehicle"
        
        # If the detection matches one of our vehicle categories, update counts and annotate
        if category is not None:
            vehicle_counts[category] += 1
            # Choose color: red for emergency vehicles, green for others
            color = (0, 0, 255) if category == "emergency vehicle" else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{category} ({conf:.2f})", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # ----- Combine Lane Detection and YOLO Results -----
    # Blend the lane detection overlay with the vehicle detection frame.
    combined_frame = cv2.addWeighted(frame, 0.8, lane_frame, 0.2, 0)
    
    return combined_frame, vehicle_counts

def calculate_green_time(counts):
    """
    Calculate the total green light duration for the lane.
    (Only includes counts for 2-wheelers, cars, and large vehicles.)
    """
    total_time = (counts["2-wheeler"] * time_assignment["2-wheeler"] +
                  counts["car"] * time_assignment["car"] +
                  counts["large vehicle"] * time_assignment["large vehicle"])
    return total_time

def adjust_traffic_signal(final_counts):
    """
    Determine traffic state and signal time based on cumulative counts.
    Emergency vehicles are prioritized.
    """
    if final_counts["emergency vehicle"] > 0:
        traffic_state = "Emergency Mode: Green for Emergency Route"
        signal_time = 30  # Example: Shorter waiting time to clear the path
    else:
        traffic_state = "Normal Operation"
        signal_time = calculate_green_time(final_counts)
    return traffic_state, signal_time

##############################################
# 4. MAIN PROCESSING LOOP
##############################################

# Open the video stream (replace with 0 for webcam or the proper video file path)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

# Get video properties (frames per second)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
frames_per_check = int(frame_rate)  # Process one frame per second for cumulative counts

# Initialize cumulative vehicle counts
final_counts = {"2-wheeler": 0, "car": 0, "large vehicle": 0, "emergency vehicle": 0}
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame
    annotated_frame, vehicle_counts = process_frame(frame)

    # If an emergency vehicle is detected in the frame, save the annotated frame immediately
    if vehicle_counts["emergency vehicle"] > 0:
        timestamp = int(time.time())
        save_path = os.path.join(save_dir, f"emergency_capture_{frame_count}_{timestamp}.jpg")
        cv2.imwrite(save_path, annotated_frame)
        print(f"Emergency vehicle detected! Saved capture to {save_path}")

    if frame_count % frames_per_check == 0:
        # Update cumulative counts
        for key in final_counts:
            final_counts[key] += vehicle_counts.get(key, 0)
        
        # Calculate green time and determine traffic state
        traffic_state, signal_time = adjust_traffic_signal(final_counts)
        print(f"Vehicle Counts: {final_counts} | Estimated Green Light Duration: {signal_time} seconds")
    
    # Overlay the traffic state and signal time info
    cv2.putText(annotated_frame, f"State: {traffic_state}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(annotated_frame, f"Green Time: {signal_time}s", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.imshow("Smart Traffic Management", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

# Final Report
traffic_state, signal_time = adjust_traffic_signal(final_counts)
print("\nFinal Report:")
print(f"Final Vehicle Count: {final_counts}")
if final_counts["emergency vehicle"] > 0:
    print("Emergency vehicles detected. Lane remains prioritized until they pass.")
else:
    print(f"Total Green Light Duration for the lane should be: {signal_time} seconds")