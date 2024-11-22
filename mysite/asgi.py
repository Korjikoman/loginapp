"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from django.urls import re_path
import app.consumers
import recognition.consumers



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from app.consumers import NotificationConsumer
from recognition.consumers import TranscriptionConsumer
# from recognition.routing import websocket_urlpatterns

websocket_urlpatterns = [re_path('ws/transcribe_audio/', TranscriptionConsumer.as_asgi()),
                re_path("ws/notify/", NotificationConsumer.as_asgi()),]


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(        
        URLRouter(
                websocket_urlpatterns
            )
    ),
})
