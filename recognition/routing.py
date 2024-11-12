from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/transcribe_audio/', consumers.TranscriptionConsumer.as_asgi())
]