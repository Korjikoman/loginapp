from channels.routing import ProtocolTypeRouter, URLRouter
from recognition.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "websocket" : websocket_urlpatterns,
})