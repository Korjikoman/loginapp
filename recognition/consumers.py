import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time

class TranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept() # accepting WebSocket connection
    
    async def disconnect(self, close_code):
        pass
    
    async def send_text(self, text):
        await self.send(text_data=json.dumps({
            'message':text
        }))