import json
from channels.generic.websocket import WebsocketConsumer
import random
from time import sleep
class TranscriptionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(100):
            self.send(json.dumps({'message': random.randint(1,100)}))
            sleep(1)
        
    def send_json(self, text_data):
        self.connect()
        text_data_json = json.loads(text_data)
        text_message = text_data_json["message"]
        self.send(text_data={
            'message' : text_message
        })
