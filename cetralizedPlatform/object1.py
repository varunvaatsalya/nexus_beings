import cv2
import torch
import numpy as np
from ultralytics import YOLO

class RealTimeObjectTracker:
    def __init__(self, model_path='yolov8n.pt'):
        # Use nano model for maximum speed
        self.model = YOLO(model_path)
        
        # Set up tracking parameters
        self.tracked_objects = {}
        self.target_classes = [24, 26, 28]  # Bag-related classes
        
        # Performance optimization
        self.model.fuse()
        
    def process_frame(self, frame):
        # Resize frame for faster processing
        frame_resized = cv2.resize(frame, (640, 360))
        
        # Perform detection with minimal overhead
        results = self.model(frame_resized, conf=0.3, iou=0.5, max_det=5)
        
        # Process detections
        for detection in results[0].boxes:
            cls = int(detection.cls)
            conf = float(detection.conf)
            
            # Filter for target classes
            if cls in self.target_classes and conf > 0.3:
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, detection.xyxy[0].tolist())
                
                # Draw bounding box
                color = (0, 255, 0)  # Green for detected objects
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
                
                # Add class label
                label = f"{self.model.names[cls]} ({conf:.2f})"
                cv2.putText(frame_resized, label, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame_resized

def main():
    # Open webcam
    cap = cv2.VideoCapture("http://192.168.244.14:4747/video")
    
    # Check if camera opens successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Set camera properties for performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Initialize tracker
    tracker = RealTimeObjectTracker()
    
    frame_counter = 0  # Initialize frame counter
    frames_to_skip = 15  # Process only every 15th frame for 2 FPS
    
    while True:
        # Read frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        # Increment frame counter
        frame_counter += 1
        
        # Process only every 15th frame
        if frame_counter % frames_to_skip == 0:
            processed_frame = tracker.process_frame(frame)
            cv2.imshow('Real-Time Object Tracking', processed_frame)
        # else:
        #     # Show original frame without processing
        #     cv2.imshow('Real-Time Object Tracking', frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



# import cv2
# import torch
# import numpy as np
# from ultralytics import YOLO

# class RealTimeObjectTracker:
#     def __init__(self, model_path='yolov8n.pt'):
#         # Use nano model for maximum speed
#         self.model = YOLO(model_path)
        
#         # Set up tracking parameters
#         self.tracked_objects = {}
#         self.target_classes = [24, 26, 28]  # Bag-related classes
        
#         # Performance optimization
#         self.model.fuse()
        
#     def process_frame(self, frame):
#         # Resize frame for faster processing
#         frame_resized = cv2.resize(frame, (640, 360))
        
#         # Perform detection with minimal overhead
#         results = self.model(frame_resized, conf=0.3, iou=0.5, max_det=5)
        
#         # Process detections
#         for detection in results[0].boxes:
#             cls = int(detection.cls)
#             conf = float(detection.conf)
            
#             # Filter for target classes
#             if cls in self.target_classes and conf > 0.3:
#                 # Get bounding box coordinates
#                 x1, y1, x2, y2 = map(int, detection.xyxy[0].tolist())
                
#                 # Draw bounding box
#                 color = (0, 255, 0)  # Green for detected objects
#                 cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
                
#                 # Add class label
#                 label = f"{self.model.names[cls]} ({conf:.2f})"
#                 cv2.putText(frame_resized, label, (x1, y1 - 10), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
#         return frame_resized

# def main():
#     # Open webcam
#     cap = cv2.VideoCapture("http://192.168.244.14:4747/video")
    
#     # Check if camera opens successfully
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return
    
#     # Set camera properties for performance
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
#     cap.set(cv2.CAP_PROP_FPS, 30)
    
#     # Initialize tracker
#     tracker = RealTimeObjectTracker()
    
#     while True:
#         # Read frame
#         ret, frame = cap.read()
        
#         if not ret:
#             print("Failed to grab frame")
#             break
        
#         # Process and display frame
#         processed_frame = tracker.process_frame(frame)
        
#         cv2.imshow('Real-Time Object Tracking', processed_frame)
        
#         # Exit on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     # Clean up
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
