import json
from channels.generic.websocket import WebsocketConsumer
import random
from time import sleep
class TranscriptionConsumer(WebsocketConsumer):
    async def connect(self):
        
        await self.channel_layer.group_add("transcriptions", self.channel_name)        
        await self.accept()
        
        for i in range(100):
            await self.send(json.dumps({'message': random.randint(1,100)}))
            sleep(1)
    async def disconnect(self, close_code):
        self.channel_layer.group_discard("transcriptions", self.channel_name)
        
    async def send_transcription(self, event):
        message = event["message"]
        self.send(text_data={
            'message' : message
        })
