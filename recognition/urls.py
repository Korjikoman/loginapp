from django.urls import path
from . import views

urlpatterns = [
    path("transcribe/", views.index, name="transcribe_audio")
]
