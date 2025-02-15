import cv2
import time
import face_recognition
import numpy as np
from threading import Thread
import requests
from PIL import Image


database = [
        #  "Gaurav": "Database/Gaurav.jpg",
        # "Alia": "Database/Alia.png",
        {
         "name":"Pratham",
         "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1732727490/YelpCamp/coehrxur5ohi2tcstkrx.jpg"
        },
        # {
        #  "name":"Satvic",
        #  "url":"Database\Satvic.jpg"
        # },
        # {
        #  "name":"Gaurav",
        #  "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733052254/YelpCamp/c8ecfad01b21309551890fb7bbbf5aa9_pqfea5.jpg"
        # }
        # "Satvic": "Database/Satvic.jpg",
]

def load_image_from_url(url):
    """
    Loads an image from a URL directly into a format compatible with face_recognition.
    """
    try:
        # Fetch the image from the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for request errors

        # Open the image using Pillow
        image = Image.open(response.raw).convert("RGB")
        
        # Convert to numpy array (compatible with face_recognition)
        return np.array(image)
    except Exception as e:
        print(f"Error loading image from URL {url}: {e}")
        return None


def detect_known_persons(cameras, tolerance=0.6, runtime=30):

    def load_known_faces():
        
        known_face_encodings = []
        known_face_names = []
        for person in database:
            name = person["name"]
            img_path = person["url"]
            if not img_path or not isinstance(img_path, str):
                print(f"Invalid path for {name}: {img_path}")
                continue
            
            if img_path.startswith("http://") or img_path.startswith("https://"):
                image = load_image_from_url(img_path)
            else:
                if not cv2.haveImageReader(img_path):
                    print(f"Image not found or invalid format: {img_path}")
                    continue

                image = face_recognition.load_image_file(img_path)
            if image is not None:

                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])  # Assume one face per image
                    known_face_names.append(name)
                else:
                    print(f"No face detected in image: {img_path}")
            else:
                print(print(f"Failed to load image for {name}: {img_path}"))
        return known_face_encodings, known_face_names


    def process_camera(camera_id, known_face_encodings, known_face_names,stop_signal, process_every_nth_frame=45):
    
   
        cap = cv2.VideoCapture(camera_id)
        frame_count = 0
        process_every_nth_frame = 45 
        detected_results[camera_id] = []
        print("Starting Search...")
        while not stop_signal[0]:

            ret, frame = cap.read()
            if not ret:
                break
            frameS = cv2.resize(frame,(0,0),None,0.25,0.25)
            # Convert to RGB (face_recognition requires RGB images)
            frameS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if frame_count % process_every_nth_frame == 0:
                
                        
                face_locations = face_recognition.face_locations(frameS, model="hog")
                face_encodings = face_recognition.face_encodings(frameS, face_locations,1,"large")

                face_names = []
                for face_encoding, faceLoc in zip(face_encodings,face_locations):
                    # Compare with known facesq
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    faceDis = face_recognition.face_distance(known_face_encodings,face_encoding)
                    matchidx = np.argmin(faceDis)
                    print(camera_id)
                    print(faceDis)
                    name = "Finding a match..."
                    if matches[matchidx] and faceDis[matchidx]<0.52:
                        name = known_face_names[matchidx]
                        
                            
                    
                    face_names.append(name)
                
                    detected_results[camera_id].extend(face_names)
                    

            # Draw rectangles and names
            for (y1, x2, y2, x1), name in zip(face_locations, face_names):
                # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1+6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
            frame_count += 1

            # Display the video feed
            cv2.imshow(f"Face Detection and Matching (HOG) - Camera {camera_id}", frame)
            
            # # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        # cv2.destroyAllWindows()

    # Load known faces
    def stop_on_input(stop_signal):
        """
        Monitor user input and set the stop signal when 'q' is pressed.
        """
        input("Press Enter to start and type 'q' then Enter anytime to stop the program.")
        while True:
            user_input = input("Type 'q' and press Enter to stop: ").strip().lower()
            if user_input == 'q':
                stop_signal[0] = True
                break

    # Load known faces
    known_face_encodings, known_face_names = load_known_faces()

    # Shared dictionary for storing results
    detected_results = {}

    # Stop signal to end threads
    stop_signal = [False]

    # Start threads for cameras
    threads = []
    for camera_id in cameras:
        thread = Thread(target=process_camera, args=(camera_id,known_face_encodings, known_face_names, stop_signal))
        thread.start()
        threads.append(thread)

    # Start stop signal thread
    input_thread = Thread(target=stop_on_input, args=(stop_signal,))
    input_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    input_thread.join()

    return detected_results

# Example Usage
if __name__ == "__main__":
    # Example database with names and image paths
#     database = [
#         #  "Gaurav": "Database/Gaurav.jpg",
#         # "Alia": "Database/Alia.png",
#         {
#          "name":"Pratham",
#          "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1732727490/YelpCamp/coehrxur5ohi2tcstkrx.jpg"
#         },
#         # {
#         #  "name":"Satvic",
#         #  "url":"Database\Satvic.jpg"
#         # },
#         # {
#         #  "name":"Gaurav",
#         #  "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733052254/YelpCamp/c8ecfad01b21309551890fb7bbbf5aa9_pqfea5.jpg"
#         # }
#         # "Satvic": "Database/Satvic.jpg",
# ]

    def push_to_global_array(): 
        time.sleep(20) # Wait for 20 seconds 
        new_object = {
         "name":"Gaurav",
         "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733052254/YelpCamp/c8ecfad01b21309551890fb7bbbf5aa9_pqfea5.jpg"
        }
        database.append(new_object) 
        print(f"Object {new_object} added to global_array: {database}")


    # List of camera IDs or IP URLs
    camera_list = ["http://192.168.244.14:4747/video","http://192.168.79.115:4747/video"]

    # Call the function to detect known persons

    Thread(target=push_to_global_array).start()
    results = detect_known_persons(camera_list, runtime=30)
    print("Detection Results:")
    print(results)