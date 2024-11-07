import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time

class TranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_text"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept() # accepting WebSocket connection
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )
    
    async def send_text(self, text):
        await self.send(text_data=json.dumps({
            'message' : text
        }))