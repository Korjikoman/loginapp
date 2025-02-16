from django.urls import path
from . import views

urlpatterns = [
    path("transcribe_audio/", views.index, name="transcribe_audio"),
    path("stop_recognition/", views.stop_recognition, name="stop_recognition")
]
