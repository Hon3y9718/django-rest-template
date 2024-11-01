import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from user.models import User
from asgiref.sync import sync_to_async

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room ID from the URL and use it as the group name
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']  # Assume user ID is passed in data

        # Retrieve the user and room
        user = await self.get_user(user_id)
        room = await self.get_room(self.room_id)

        # Save message to database
        if user and room:
            new_message = await sync_to_async(Message.objects.create)(
                room=room,
                sender=user,
                message=message
            )

            # Broadcast the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': user.username,
                    'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def get_room(self, room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None
