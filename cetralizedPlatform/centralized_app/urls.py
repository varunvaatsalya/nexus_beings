from django.urls import path
from .views import add_report, add_cam, streams
from .views import detect_known_persons, get_person_request,getCheck
getCheck

urlpatterns = [
    path('add-report/', add_report, name='add_report'),  # Endpoint to add face
    path('add-cam/', add_cam, name='add_cam'),  # Endpoint to add face
    path('detect/', detect_known_persons, name='detect_known_persons'),  # Endpoint to add face
    path('streams/', streams, name='streams'),  # Endpoint to add face
    path('database/', get_person_request, name='get_person_request'),  # Endpoint to add face
    path('check/', getCheck, name='getCheck'),  # Endpoint to add face
]


