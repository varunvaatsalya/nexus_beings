# from django.http import JsonResponse
# import json
# from django.views.decorators.csrf import csrf_exempt
# from threading import Thread
# import cv2
# import face_recognition
# import numpy as np
# from PIL import Image
# import requests
# import asyncio
# import time

# database = {
#     "6jbhush87njeu8" : {"name":"Pratham","url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1732727490/YelpCamp/coehrxur5ohi2tcstkrx.jpg"},
#     "6jbhush87bdgdknk8":{ "name":"Gaurav",
#          "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733052254/YelpCamp/c8ecfad01b21309551890fb7bbbf5aa9_pqfea5.jpg"}
# }
# known_face_encodings = []
# known_face_names = []
# chk = 1
#     # List of camera IDs or IP URLs
# cameras = [{"name": 'varun', "url": "http://192.168.79.115:4747/video", "camId": 'tdwhgd'}]
# stop_signal = [False]
# def load_image_from_url(url):
#     """
#     Loads an image from a URL directly into a format compatible with face_recognition.
#     """
#     try:
#         # Fetch the image from the URL
#         response = requests.get(url, stream=True)
#         response.raise_for_status()  # Check for request errors

#         # Open the image using Pillow
#         image = Image.open(response.raw).convert("RGB")
        
#         # Convert to numpy array (compatible with face_recognition)
#         return np.array(image)
#     except Exception as e:
#         print(f"Error loading image from URL {url}: {e}")
#         return None




# @csrf_exempt
# def add_report(request):
#     global chk
#     # global known_face_encodings, known_face_names
#     if request.method == "GET":
#         return JsonResponse({"message": "HELLO Mr. GAURAV JII"}, status=200)
    
#     elif request.method == "POST":
#         print("api hitted")
#         try:
#             data = json.loads(request.body)
#             chk = 0
#             name = data.get("name")
#             url = data.get("url")
#             reportId = data.get("reportId")
#             new_person = {"name": name, "url": url}
#             database[reportId] = new_person
#             print('database')
#             print(database)
#             load_known_faces()
#             print('After api hitting',known_face_names)
#             if not name or not url:
#                 return JsonResponse({"error": "Name and URL are required."}, status=400)
        
#             # success, message = add_known_person(name, url)
#             # if success:
#             return JsonResponse({"message": "message", "name": name, "url": url}, status=200)
#             # else:
#             #     return JsonResponse({"error": message}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=400)

# @csrf_exempt
# def add_cam(request):

#     if request.method == "GET":
#         return JsonResponse({"message": "HELLO Mr. GAURAV JII"}, status=200)

#     elif request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             name = data.get("name")
#             url = data.get("url")
#             camId = data.get("camId")
#             new_cam = {"name": name, "url": url, "camId": camId}
#             cameras.append(new_cam)
#             # print(new_cam)

#             if not name or not url or not camId:
#                 return JsonResponse({"error": "Name and URL are required."}, status=400)
        
#             # success, message = add_known_person(name, url)
#             # if success:
#             print('cameras:')
#             print(cameras)
#             return JsonResponse({"message": "camera added successfully", "name": name, "url": url, "camId": camId}, status=200)
#             # else:
#             #     return JsonResponse({"error": message}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=400)



# def send_post_request(camId, reportId):
#     data_to_send = {
#         'camId':camId,
#         "reportId": reportId,
#     }

#     # Doosre server ka URL yaha likhein
#     url = "http://192.168.244.24:5000/personDetected"
#     # url = "https://server-sih-1.onrender.com/personDetected"

#     try:
#         # POST request bhejna
#         response = requests.post(url, json=data_to_send)
#         print(response);
#         # Response ka status check karein
#         if response.status_code == 200:
#             print({"message": "POST request successful", "response": response.json()})
#         else:
#             print({"message": "Failed to send POST request", "response": response.status})
    
#     except requests.exceptions.RequestException as e:
#         # Agar koi error aaye to handle karein
#         print({"message": "An error occurred", "error": str(e)})

# def load_known_faces():
#         global known_face_encodings
#         global known_face_names

#         for reportid in database:
#             name = reportid
#             img_path = database[reportid]["url"]
#             if not img_path or not isinstance(img_path, str):
#                 print(f"Invalid path for {name}: {img_path}")
#                 continue
            
#             if img_path.startswith("http://") or img_path.startswith("https://"):
#                 image = load_image_from_url(img_path)
#             else:
#                 if not cv2.haveImageReader(img_path):
#                     print(f"Image not found or invalid format: {img_path}")
#                     continue

#                 image = face_recognition.load_image_file(img_path)
#             if image is not None:

#                 encodings = face_recognition.face_encodings(image)
#                 if encodings:
#                     known_face_encodings.append(encodings[0])  # Assume one face per image
#                     known_face_names.append(name)
#                 else:
#                     print(f"No face detected in image: {img_path}")
#             else:
#                 print(print(f"Failed to load image for {name}: {img_path}"))
#         # return known_face_encodings, known_face_names


# def detect_known_persons(tolerance=0.5):
    
#     def process_camera(camera, stop_signal):

#         global known_face_encodings
#         global known_face_names
#         global chk
#         camera_id = camera["url"]
#         cap = cv2.VideoCapture(camera_id)
#         frame_count = 0
#         process_every_nth_frame = 45 
#         while not stop_signal[0]:
#             ret, frame = cap.read()
#             if not ret:
#                 print(f"Camera {camera_id} not accessible or stream ended.")
#                 break

#             # Resize and convert frame for processing
#             # frameS = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#             frameS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             # Process every nth frame
#             if frame_count % process_every_nth_frame == 0:
#                 print('inside process cam',known_face_names)
#                 print('inside process cam',database)
#                 face_locations = face_recognition.face_locations(frameS, model="hog")
#                 face_encodings = face_recognition.face_encodings(frameS, face_locations,1,"large")
#                 face_names = []
#                 for face_encoding,faceLoc in zip(face_encodings,face_locations):
#                     matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
#                     print("MATCHES",matches)
#                     face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                     matchidx = np.argmin(face_distances)
#                     name = "Finding a match"
#                     if matches[matchidx] and face_distances[matchidx]<0.52:
#                         # best_match_index = np.argmin(face_distances)
#                         reportid = known_face_names[matchidx]
#                         name = database[reportid]["name"]
#                         print(f"{name} detected on Camera: {camera_id}")
#                         camId = camera["camId"]
#                         # send_post_request(camId,reportid)

#                         # if camera_id not in detected_results:
#                         #     detected_results[camera_id] = []
#                         # if name not in detected_results[camera_id]:
#                         #     detected_results[camera_id].append(name)
#                     face_names.append(name)
#             for (y1,x2,y2,x1), name in zip(face_locations,face_names):
#                 cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
#                 cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
#             frame_count += 1
#             cv2.imshow(f'Camera {camera_id}', frame)

#         # Break on 'q' key press or if camera is inaccessible
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cap.release()
    

#     # Load known faces
#     def stop_on_input(stop_signal):
#         """
#         Monitor user input and set the stop signal when 'q' is pressed.
#         """
#         print("Press Enter to start and type 'q' then Enter anytime to stop the program.")
#         while True:
#             user_input = input("Type 'q' and press Enter to stop: ").strip().lower()
#             if user_input == 'q':
#                 stop_signal[0] = True
#                 break

#     # Load known faces
#     load_known_faces()

#     # Shared dictionary for storing results
#     # detected_results = {}

#     # Stop signal to end threads
#     # stop_signal = [False]

#     # Start threads for cameras
#     # threads = []
#     for camera in cameras:
#         process_camera(camera, stop_signal)

#     # Start stop signal thread
    

#     # return detected_results

#     # Call the function to detect known persons


# KUNAL SIR --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# from django.http import JsonResponse
# import json
# from django.views.decorators.csrf import csrf_exempt
# from threading import Thread
# import cv2
# import face_recognition
# import numpy as np
# from PIL import Image
# import requests
# import time

# class FaceDatabase:
#     def __init__(self):
#         self.known_face_encodings = []
#         self.known_face_names = []

# face_database = FaceDatabase()

# database = {
#     "6jbhush87njeu8": {
#         "name": "Pratham",
#         "url": "https://res.cloudinary.com/dcbrfuldz/image/upload/v1732727490/YelpCamp/coehrxur5ohi2tcstkrx.jpg"
#     }
# }

# cameras = [{"name": 'varun', "url": "http://192.168.79.115:4747/video", "camId": 'tdwhgd'}]
# stop_signal = [False]

# def load_image_from_url(url):
#     try:
#         response = requests.get(url, stream=True)
#         response.raise_for_status() 
#         image = Image.open(response.raw).convert("RGB")
#         return np.array(image)
#     except Exception as e:
#         print(f"Error loading image from URL {url}: {e}")
#         return None


# def load_all_faces_into_database():
#     """Load all faces from 'database' into face_database."""
#     face_database.known_face_encodings.clear()
#     face_database.known_face_names.clear()

#     for reportid, person_data in database.items():
#         img_url = person_data.get("url")
#         if not img_url:
#             print(f"Invalid path for {reportid}: {img_url}")
#             continue

#         image = load_image_from_url(img_url)
#         if image is not None:
#             encodings = face_recognition.face_encodings(image)
#             if encodings:
#                 face_database.known_face_encodings.append(encodings[0])
#                 face_database.known_face_names.append(reportid)
#             else:
#                 print(f"No face detected in image: {img_url}")
#         else:
#             print(f"Failed to load image for {reportid}: {img_url}")


# @csrf_exempt
# def add_report(request):
#     if request.method == "GET":
#         return JsonResponse({"message": "HELLO Mr. GAURAV JII"}, status=200)
    
#     elif request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             name = data.get("name")
#             url = data.get("url")
#             reportId = data.get("reportId")

#             if not name or not url or not reportId:
#                 return JsonResponse({"error": "Name, URL, and reportId are required."}, status=400)

#             database[reportId] = {"name": name, "url": url}
#             print('database updated:', database)

#             # Add the new face encoding directly to face_database
#             image = load_image_from_url(url)
#             if image is not None:
#                 encodings = face_recognition.face_encodings(image)
#                 if encodings:
#                     face_database.known_face_encodings.append(encodings[0])
#                     face_database.known_face_names.append(reportId)
#                     print('After adding new face:', face_database.known_face_names)
#                 else:
#                     print("No face found in the newly added image.")
#             else:
#                 print("Failed to load the new image.")

#             return JsonResponse({"message": "Face added successfully", "name": name, "url": url}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=400)


# @csrf_exempt
# def add_cam(request):
#     if request.method == "GET":
#         return JsonResponse({"message": "HELLO Mr. GAURAV JII"}, status=200)

#     elif request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             name = data.get("name")
#             url = data.get("url")
#             camId = data.get("camId")

#             if not name or not url or not camId:
#                 return JsonResponse({"error": "Name, URL and camId are required."}, status=400)

#             new_cam = {"name": name, "url": url, "camId": camId}
#             cameras.append(new_cam)
#             print('cameras updated:', cameras)
#             return JsonResponse({"message": "camera added successfully", "name": name, "url": url, "camId": camId}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=400)


# def send_post_request(camId, reportId):
#     data_to_send = {
#         'camId': camId,
#         "reportId": reportId,
#     }

#     url = "http://192.168.244.24:5000/personDetected"

#     try:
#         response = requests.post(url, json=data_to_send)
#         if response.status_code == 200:
#             print({"message": "POST request successful", "response": response.json()})
#         else:
#             print({"message": "Failed to send POST request", "response": response.status})
#     except requests.exceptions.RequestException as e:
#         print({"message": "An error occurred", "error": str(e)})


## VARUN CODE

def streams(tolerance=0.5):
    def process_camera(camera, stop_signal):
        camera_id = camera["url"]
        cap = cv2.VideoCapture(camera_id)
        frame_count = 0
        process_every_nth_frame = 45 

        while not stop_signal[0]:
            ret, frame = cap.read()
            if not ret:
                print(f"Camera {camera_id} not accessible or stream ended.")
                break

            frameS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if frame_count % process_every_nth_frame == 0:
                known_face_encodings = face_database.known_face_encodings
                known_face_names = face_database.known_face_names
                print('inside process cam, known faces:', known_face_names)
                face_locations = face_recognition.face_locations(frameS, model="hog")
                face_encodings = face_recognition.face_encodings(frameS, face_locations, 1, "large")
                face_names = []

                for face_encoding, faceLoc in zip(face_encodings, face_locations):
                    if not known_face_encodings:
                        # If no known faces, skip
                        face_names.append("No known faces")
                        continue

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    matchidx = np.argmin(face_distances)
                    name = "Unknown"

                    if matches[matchidx] and face_distances[matchidx]<0.52:
                        reportid = known_face_names[matchidx]
                        name = database[reportid]["name"]
                        print(f"{name} detected on Camera: {camera_id}")
                        camId = camera["camId"]
                        # Uncomment to send a POST request on detection
                        # send_post_request(camId, reportid)
                    face_names.append(name)

                for (y1,x2,y2,x1), name in zip(face_locations, face_names):
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

            frame_count += 1
            cv2.imshow(f'Camera {camera_id}', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    # Load known faces initially
    load_all_faces_into_database()

    for camera in cameras:
        process_camera(camera, stop_signal)

        
# YASH CODE ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import requests
from face_recognition_app.models import FaceData
from threading import Thread
import cv2
import face_recognition
from PIL import Image
import asyncio
import aiohttp
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
import cloudinary 
import cloudinary.uploader
from django.views.decorators.http import require_http_methods

database = {
    # "675960bf0c21716935e3b79d" : {"name":"Gaurav","url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733910719/YelpCamp/3474ce1a9d78cecbe3f5fcb2c0d178b1_mc6pms.jpg"},
    # "182egh198fv913g9g193g3gd" : {"name":"Nikita","url":"https://res.cloudinary.com/ddv1qs3by/image/upload/v1733985536/Detected_faces/l2gfousq5at5d3eoyhi4.jpg"}
    # "6jbhush87bdgdknk8":{ "name":"Gaurav",
    #      "url":"https://res.cloudinary.com/dcbrfuldz/image/upload/v1733052254/YelpCamp/c8ecfad01b21309551890fb7bbbf5aa9_pqfea5.jpg"}
}
cloudinary.config(
    cloud_name="ddv1qs3by",
    api_key="393969885467845",
    api_secret="frN47r85mTKTJ65hDv-wQBvdXMU"
)

    # List of camera IDs or IP URLs//675a9310f66b18c8e096d8c4
cameras = [{"name": 'CAM1', "url": "http://192.168.137.167:4747/video", "camId": '674c39e06bbf9f8c18ad1ef0'}]

# for report in response["data"]:
            #     database[report._id] = {
            #         "name":report.name,
            #         "url":report.url,
            #     }

@csrf_exempt
def getCheck(request):
    if request.method == "GET":
        return JsonResponse({"success": True}, status=200)
    elif request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        return JsonResponse({"success": True, "name":name}, status=200)

# @require_http_methods(["GET"])
@csrf_exempt
def get_person_request(request):
    if request.method == "GET":
        url = "http://192.168.137.8:5000/getMissingPersons"

        try:
            # Sending the GET request to the Node server
            response = requests.get(url)
            # print(response)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response JSON
                reports = response.json() 
                for report in reports["data"]:
                    reportId = report["_id"]
                    database[reportId] = {
                        "name":report["name"],
                        "url":report["url"],
                    # print(report)
                }
            #  # Ensure the response content is JSON
                # print("Success:", data["data"])
                print(database)
                # Return the data as a JsonResponse
                return JsonResponse({"success": True, "data": reports}, status=200)
            else:
                print("Failed with status:", response.status_code)
                return JsonResponse({"success": False, "error": "Failed to fetch data"}, status=response.status_code)
        
        except requests.exceptions.RequestException as e:
            # Handle request errors
            print("An error occurred:", str(e))
            return JsonResponse({"success": False, "error": "An error occurred while making the request"}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

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

async def process_faces(database):
    print("Inside process_faces thread")
    try:
        face_encodings, face_names = await load_known_faces(database)
        print("Done encoding inside process_faces", face_names)
        await save_new_face_data(face_names, face_encodings)
        print("Background processing completed successfully.")
    except Exception as e:
        print(f"Error in background processing: {e}")


@csrf_exempt
async def add_report(request):
    if request.method == "GET":
        return JsonResponse({"message": "HELLO Mr. GAURAV VISHWAKARMA JII"}, status=200)

    elif request.method == "POST":
        print("api hitted")
        try:
            try:
                url = "http://localhost:6000/toggle-variable"
                payload = {"key": "value"}
                # response = requests.get(url) 
                # response_data = response.json()
                async with aiohttp.ClientSession() as session: 
                    async with session.post(url, json=payload) as response: 
                        response_data = await response.json()
                        flag = response_data["flag"]
                        print("Updated value of flag at start of add_report function is", flag)
            except requests.RequestException as e:
                print(f"RequestException occurred: {e}")

            data = json.loads(request.body)
            name = data.get("name")
            url = data.get("url")
            reportId = data.get("reportId")
            new_person = {"name": name, "url": url}
            # database.clear()
            print("database :", database)
            database[reportId] = new_person
            print('database')
            print(database)
            # JsonResponse({"message": "message", "name": name, "url": url}, status=200)

            face_encodings, face_names = await load_known_faces(database)
            # asyncio.create_task(process_faces(database))
            # face_encodings, face_names = await load_known_faces({
            #     reportId:{
            #         new_person
            #     }
            # })
            await save_new_face_data(face_names, face_encodings)
            print('New faces saved successfully', face_names)
            # except Exception as e:
            #     print(f"Error while processing faces: {e}")
            #     return JsonResponse({"error": "Error while processing faces."}, status=500)

            # print(new_person)
            
            # known_face_names, known_face_encodings = get_face_data()
            # print('known_face_names inside add_report after saving ', known_face_names)
            # if not name or not url:
            #     return JsonResponse({"error": "Name and URL are required."}, status=400)
        
            # success, message = add_known_person(name, url)
            # if success:
            # url = "https://varunvaatsalya.vercel.app/api/flag?update=1" 
            try: 
                url = "http://localhost:6000/toggle-variable"
                payload = {"key": "value"}
                # response = requests.get(url) 
                # response_data = response.json()
                async with aiohttp.ClientSession() as session: 
                    async with session.post(url, json=payload) as response: 
                        response_data = await response.json()
                        flag = response_data["flag"]
                        print("Updated value of flag at start of add_report function is", flag)
                flag = response_data["flag"]
                print("Updated value of flag at end of add_report function is", flag)
            except requests.RequestException as e:
                print(f"RequestException occurred: {e}")

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

def send_post_request(camId, reportId,url):
    data_to_send = {
        'camId':camId,
        "reportId": reportId,
        "url":url,
    }

    # Doosre server ka URL yaha likhein

    # url = "http://172.16.224.33:5000/personDetected"
    # url = "http://192.168.244.24:5000/personDetected"
    url = "http://192.168.137.8:5000/personDetected"
    # url = "https://server-sih-1.onrender.com/personDetected"

    try:
        # POST request bhejna
        response = requests.post(url, json=data_to_send)
        print(response);
        # Response ka status check karein
        if response.status_code == 200:
            print("sucess")
            # print({"message": "POST request successful", "response": response.json()})
        else:
            # print({"message": "Failed to send POST request", "response": response.status})
            print("false")
    
    except requests.exceptions.RequestException as e:
        # Agar koi error aaye to handle karein
        print({"message": "An error occurred", "error": str(e)})
try:
    async def load_known_faces(database):
        print("Inside load_known_faces")
        print(f"Database contents: {database}")

        known_face_encodings = []
        known_face_names = []

        database_copy = database.copy()  # Clone to avoid race conditions

        for reportid in database_copy:
            name = reportid
            img_path = database_copy[reportid]["url"]
            
            # print(img_path)
            if not img_path or not isinstance(img_path, str):
                print(f"Invalid path for {name}: {img_path}")
                continue
            
            try:
                # Load the image from URL or local path
                if img_path.startswith("http://") or img_path.startswith("https://"):
                    image = load_image_from_url(img_path)
                    # print(image)
                else:
                    if not cv2.haveImageReader(img_path):
                        # print(f"Image not found or invalid format: {img_path}")
                        continue
                    image = face_recognition.load_image_file(img_path)

                if image is None:
                    print(f"Failed to load image for {name}: {img_path}")
                    continue

                print('Before encoding inside load_known_faces')

                # Perform face encoding in a separate thread
                # print("Printing image before encoding", image)
                encodings = await asyncio.to_thread(face_recognition.face_encodings, image)
                # print(f"Encoding complete for {name}. Encodings: {encodings}")

                if encodings:
                    print('Got encoding inside load_known_faces')
                    known_face_encodings.append(encodings[0])  # Assume one face per image
                    known_face_names.append(name)
                else:
                    print(f"No face detected in image: {img_path}")

            except Exception as e:
                print(f"Error processing {name} at {img_path}: {e}")
                continue

        return known_face_encodings, known_face_names
except Exception as e:
    print(f"Error loading known faces: {e}")

async def detect_known_persons( tolerance=0.5):

    async def process_camera(camera, detected_results, known_face_encodings, known_face_names, stop_signal):
        
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
                 
                try: 
                    url = "http://localhost:6000/variable-state"
                    # response = requests.get(url) 
                    # response_data = response.json()
                    async with aiohttp.ClientSession() as session: 
                        async with session.get(url) as response: 
                            response_data = await response.json()
                            flag = response_data["flag"]
                            print("Updated value of flag at start of process_cam function is", flag)
                    # flag = response_data["flag"]
                    # print("Updated value of flag at start of process_cam function is", flag)
                except requests.RequestException as e:
                    print("Unable to toggle flag")
                if not flag:
                    continue
                known_face_names, known_face_encodings = await get_face_data()
                print('known_face_names inside process_cam ', known_face_names)
                face_locations = face_recognition.face_locations(frameS, model="hog")
                face_encodings = face_recognition.face_encodings(frameS, face_locations,1,"large")
                face_names = []
                for face_encoding,faceLoc in zip(face_encodings,face_locations):
                    i=0
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    # print("face_distances",face_distances)
                    matchidx = np.argmin(face_distances)
                    name = "Finding a match"
                    if matches[matchidx] and face_distances[matchidx]<0.52:
                        (top,right,bottom,left) = faceLoc[0],faceLoc[1],faceLoc[2],faceLoc[3]

                        detected_image = frame[top:bottom,left:right]
                        temp_img_path = f"Detected_Person/_{i}.jpg"

                        cv2.imwrite(temp_img_path,detected_image)
                        i=i+1
                        print("image is saved successfully..")
                        response = cloudinary.uploader.upload(temp_img_path, folder="Detected_Person/")
                        print(response['secure_url'])
                        # best_match_index = np.argmin(face_distances)
                        reportid = known_face_names[matchidx]
                        # name = database[reportid]["name"]
                        print(f"{reportid} detected on Camera: {camera_id}")
                        camId = camera["camId"]
                        send_post_request(camId,reportid,response['secure_url'])

                        if camera_id not in detected_results:
                            detected_results[camera_id] = []
                        if name not in detected_results[camera_id]:
                            detected_results[camera_id].append(name)
                    face_names.append(name)
            # for (y1,x2,y2,x1), name in zip(face_locations,face_names):
            #     cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            #     cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
            frame_count += 1
            cv2.imshow(f'Camera {camera_id}', frame)

        # Break on 'q' key press or if camera is inaccessible
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
    



    # Load known faces
    async def stop_on_input(stop_signal):
        print("Press Enter to start and type 'q' then Enter anytime to stop the program.")
        while True:
            # Run the blocking input function in a thread and await its result
            user_input = await asyncio.to_thread(input, "Type 'q' and press Enter to stop: ")
            user_input = user_input.strip().lower()  # Process the input string
            if user_input == 'q':
                stop_signal[0] = True
                break

    # Load known faces
    face_encodings, face_names = await load_known_faces(database)
    await save_new_face_data(face_names, face_encodings)
    print('known_face_names before calling process_cam inside detect_person', face_names)
    # Shared dictionary for storing results
    detected_results = {}

    # Stop signal to end threads
    stop_signal = [False]

    # Start threads for cameras
    tasks = []
    for camera in cameras:
        # thread = Thread(target = process_camera,args=)
        tasks.append(asyncio.create_task(process_camera(camera, detected_results, face_encodings, face_names, stop_signal)))

    tasks.append(asyncio.create_task(stop_on_input(stop_signal)))

    await asyncio.gather(*tasks)

    # return detected_results

    # Call the function to detect known persons

# Example data
@sync_to_async
def save_new_face_data(new_names, new_encodings):
    # Assuming you are adding this data to the first record in the FaceData model
    # You can modify this logic to create a new FaceData object if necessary
    face_data = FaceData.objects.first()  # Get the first record (or create a new one if needed)

    if face_data:
        # Append new names and encodings to the existing ones
        face_data.set_names(new_names)
        face_data.set_face_encodings(new_encodings)
        face_data.save()
    else:
        # If no face data exists, create a new entry
        face_data = FaceData(names=new_names, face_encodings=[encoding.tolist() for encoding in new_encodings])
        face_data.save()

@sync_to_async
def get_face_data():
    # Get the first FaceData object from the database
    face_data = FaceData.objects.first()
    
    if face_data:
        names = face_data.get_names()  # List of names
        encodings = face_data.get_face_encodings()  # List of face encodings as numpy arrays
        return names, encodings
    else:
        return [], []  # Return empty arrays if no data exists


