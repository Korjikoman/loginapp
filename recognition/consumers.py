import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class TranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'transcriptions'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_transcription(self, event):
        await self.send(text_data=json.dumps({ 'message': event['message'] }))
