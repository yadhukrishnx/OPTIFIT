# squats/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WorkoutConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_workout_status(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))