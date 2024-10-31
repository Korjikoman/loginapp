import json
from channels.generic.websocket import WebsocketConsumer
import time

class TranscriptionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept() # accepting WebSocket connection
    
    def disconnect(self, close_code):
        pass
    
    def send_text(self, text):
        self.send(text_data=json.dumps({
            'message':text
        }))