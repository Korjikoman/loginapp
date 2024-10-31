from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/audio_transcription/', consumers.TranscriptionConsumer.as_asgi())
]