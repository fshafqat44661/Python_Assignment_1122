from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def list_messages(self, event):
        # Fetch and send messages to the connected client
        chat_room_id = event['room_id']  # assuming room_id is sent in the event
        messages = Message.objects.filter(chat_room_id=chat_room_id)
        message_data = [{'text': message.text, 'sender': message.sender.username} for message in messages]

        # Send the messages to the WebSocket client
        await self.send(text_data=json.dumps({
            'type': 'messages.list',
            'messages': message_data,
        }))