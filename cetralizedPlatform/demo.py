


from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from threading import Thread
import cv2
import face_recognition
import numpy as np
from PIL import Image
import requests

database = {
    # "6jbhush87njeu8" : {"name":"Pratham","url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1732727490/YelpCamp/coehrxur5ohi2tcstkrx.jpg"},
    "6jbhush87bdgdknk8":{ "name":"Gaurav",
         "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733052254/YelpCamp/c8ecfad01b21309551890fb7bbbf5aa9_pqfea5.jpg"}
}

    # List of camera IDs or IP URLs
cameras = [{"name": 'varun', "url": "http://192.168.79.115:4747/video", "camId": 'tdwhgd'}]

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




@csrf_exempt
def add_face(request):
    global known_face_encodings, known_face_names

    if request.method == "GET":
        return JsonResponse({"message": "HELLO Mr. GAURAV VISHWAKARMA JII"}, status=200)

    elif request.method == "POST":
        print("api hitted")
        try:
            data = json.loads(request.body)
            name = data.get("name")
            url = data.get("url")
            reportId = data.get("reportId")
            new_person = {"name": name, "url": url}
            database[reportId] = new_person
            # print(new_person)
            print('database')
            print(database)

            if not name or not url:
                return JsonResponse({"error": "Name and URL are required."}, status=400)
        
            # success, message = add_known_person(name, url)
            # if success:
            return JsonResponse({"message": "message", "name": name, "url": url}, status=200)
            # else:
            #     return JsonResponse({"error": message}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def add_cam(request):

    if request.method == "GET":
        return JsonResponse({"message": "HELLO Mr. GAURAV VISHWAKARMA JII"}, status=200)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            url = data.get("url")
            camId = data.get("camId")
            new_cam = {"name": name, "url": url, "camId": camId}
            cameras.append(new_cam)
            # print(new_cam)

            if not name or not url or not camId:
                return JsonResponse({"error": "Name and URL are required."}, status=400)
        
            # success, message = add_known_person(name, url)
            # if success:
            print('cameras:')
            print(cameras)
            return JsonResponse({"message": "camera added successfully", "name": name, "url": url, "camId": camId}, status=200)
            # else:
            #     return JsonResponse({"error": message}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)



def send_post_request(camId, reportId):
    data_to_send = {
        'camId':camId,
        "reportId": reportId,
    }

    # Doosre server ka URL yaha likhein
    url = "http://192.168.244.24:5000/personDetected"
    # url = "https://server-sih-1.onrender.com/personDetected"

    try:
        # POST request bhejna
        response = requests.post(url, json=data_to_send)
        print(response);
        # Response ka status check karein
        if response.status_code == 200:
            print({"message": "POST request successful", "response": response.json()})
        else:
            print({"message": "Failed to send POST request", "response": response.status})
    
    except requests.exceptions.RequestException as e:
        # Agar koi error aaye to handle karein
        print({"message": "An error occurred", "error": str(e)})




def detect_known_persons( tolerance=0.5):

    def load_known_faces(database):
        
        
        known_face_encodings = []
        known_face_names = []
        for reportid in database:
            name = reportid
            img_path = database[reportid]["url"]
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

    def process_camera(camera, detected_results, known_face_encodings, known_face_names, stop_signal):
        
        camera_id = camera["url"]
        cap = cv2.VideoCapture(camera_id)
        frame_count = 0
        process_every_nth_frame = 45 
        while not stop_signal[0]:
            ret, frame = cap.read()
            if not ret:
                print(f"Camera {camera_id} not accessible or stream ended.")
                break

            # Resize and convert frame for processing
            # frameS = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            frameS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process every nth frame
            if frame_count % process_every_nth_frame == 0:
                face_locations = face_recognition.face_locations(frameS, model="hog")
                face_encodings = face_recognition.face_encodings(frameS, face_locations,1,"large")
                face_names = []
                for face_encoding,faceLoc in zip(face_encodings,face_locations):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    matchidx = np.argmin(face_distances)
                    name = "Finding a match"
                    if matches[matchidx] and face_distances[matchidx]<0.52:
                        # best_match_index = np.argmin(face_distances)
                        reportid = known_face_names[matchidx]
                        name = database[reportid]["name"]
                        print(f"{name} detected on Camera: {camera_id}")
                        camId = camera["camId"]
                        # send_post_request(camId,reportid)

                        if camera_id not in detected_results:
                            detected_results[camera_id] = []
                        if name not in detected_results[camera_id]:
                            detected_results[camera_id].append(name)
                    face_names.append(name)
            for (y1,x2,y2,x1), name in zip(face_locations,face_names):
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
            frame_count += 1
            cv2.imshow(f'Camera {camera_id}', frame)

        # Break on 'q' key press or if camera is inaccessible
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
    

    # Load known faces
    def stop_on_input(stop_signal):
        """
        Monitor user input and set the stop signal when 'q' is pressed.
        """
        print("Press Enter to start and type 'q' then Enter anytime to stop the program.")
        while True:
            user_input = input("Type 'q' and press Enter to stop: ").strip().lower()
            if user_input == 'q':
                stop_signal[0] = True
                break

    # Load known faces
    known_face_encodings, known_face_names = load_known_faces(database)

    # Shared dictionary for storing results
    detected_results = {}

    # Stop signal to end threads
    stop_signal = [False]

    # Start threads for cameras
    threads = []
    for camera in cameras:
        thread = Thread(target=process_camera, args=(camera, detected_results, known_face_encodings, known_face_names, stop_signal))
        thread.start()
        threads.append(thread)

    # Start stop signal thread
    input_thread = Thread(target=stop_on_input, args=(stop_signal,))
    input_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    input_thread.join()

    # return detected_results

    # Call the function to detect known persons

detect_known_persons()