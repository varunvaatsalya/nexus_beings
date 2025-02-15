import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
faceNet = cv2.dnn.readNet(faceModel, faceProto)

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"
genderNet = cv2.dnn.readNet(genderModel, genderProto)

genderList = ['Male', 'Female']

def getFace(faceDetectionModel, inputImage, conf_threshold=0.7):
    cpy_input_image = inputImage.copy()  # To avoid modifications to the original input

    frameWidth = cpy_input_image.shape[1]
    frameHeight = cpy_input_image.shape[0]

    blob = cv2.dnn.blobFromImage(cpy_input_image, scalefactor=1, size=(227, 227), mean=(104, 117, 123), crop=False)  # preprocessed image

    faceDetectionModel.setInput(blob)
    detections = faceDetectionModel.forward()

    bounding_boxes = []
    for i in range(detections.shape[2]):  # detections is an array having [no.of.images/batch size, classes/channels, i-th detections, confidence_score]
        confidence_score = detections[0, 0, i, 2]  # gets the confidence score for i-detections, 4-th index(value:2) shows confidence score

        if confidence_score > conf_threshold:  # get the co-ordinates of the bounding boxes only if its detected as a face, confidence score sets the minimum limit
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bounding_boxes.append([x1, y1, x2, y2])

            cv2.rectangle(cpy_input_image, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=2)
    return cpy_input_image, bounding_boxes

# Function to calculate angle
def calculate_angle(a, b, c):
    """Calculate angle between three points a, b, c (shoulder, elbow, wrist)."""
    a = np.array([a.x, a.y])  # Shoulder
    b = np.array([b.x, b.y])  # Elbow
    c = np.array([c.x, c.y])  # Wrist

    # Vector calculations
    ba = a - b
    bc = c - b

    # Compute angle
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    return np.degrees(angle)

# Function to detect distress signals
def detect_distress(landmarks):
    if landmarks is None:
        return False, None

    # Get landmark positions
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    nose = landmarks[mp_pose.PoseLandmark.NOSE]  # Reference point for head height

    # Calculate angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    # Print angles to terminal
    print(f"Left Arm Angle: {left_arm_angle:.2f}, Right Arm Angle: {right_arm_angle:.2f}")

    # Check if hands are above the head (wrist Y < nose Y)
    left_hand_above_head = left_wrist.y < nose.y
    right_hand_above_head = right_wrist.y < nose.y

    # Check distress conditions
    if (40 <= left_arm_angle <= 190 and left_hand_above_head) or (40 <= right_arm_angle <= 190 and right_hand_above_head):
        return True, "Distress Signal Detected"

    return False, None

# Open webcam
cap = cv2.VideoCapture("WhatsApp Video 2025-02-15 at 17.41.36_bf0f7896.mp4")
gender = ""
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
# Start pose estimation
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        detected_image, bounding_boxes = getFace(faceNet, frame)
        if not bounding_boxes:
        
            print("No faces detected in the image")
            out.write(frame)
        for bounding_box in bounding_boxes:
            x1, y1, x2, y2 = bounding_box
            detected_face_box = frame[y1:y2, x1:x2]

            detected_face_blob = cv2.dnn.blobFromImage(detected_face_box, scalefactor=1, size=(227, 227), mean=([78.4263377603, 87.7689143744, 114.895847746]), crop=False)

            genderNet.setInput(detected_face_blob)
            genderPrediction = genderNet.forward()

            gender = genderList[genderPrediction[0].argmax()]
            print(gender)
        # Convert BGR to RGB for MediaPipe
        if gender == "Female":
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True

        # Convert back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Detect distress signals
                detected, message = detect_distress(results.pose_landmarks.landmark)
                if detected:
                    cv2.putText(image, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Display video
            cv2.imshow("Distress Detection", image)
            out.write(image)
            # Exit on 'q'
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

# Release resources
cap.release()
cv2.destroyAllWindows()