from django.apps import AppConfig
from threading import Thread
# from .views import get_missing_person_request
# import threading

# class FaceRecognitionAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'face_recognition_app'

# def ready(self):
#     Thread(target=get_missing_person_request, daemon=True).start()
#     # def ready(self):
#     #     Thread(target=sih, daemon=True).start()


# class FaceRecognitionAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'face_recognition_app'

#     def ready(self):
#         global detection_thread
#         detection_thread = threading.Thread(target=detect_known_persons, daemon=True)
#         detection_thread.start()
