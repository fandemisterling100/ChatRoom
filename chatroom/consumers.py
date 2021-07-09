import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, User
from bot.interfaces import _BotInterface


class ChatroomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # To accept connection call
        await self.accept()

    async def disconnect(self, close_code):
        # The user leave the room (called when the socket closes)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from websocket
    async def receive(self, text_data):
        # Decode JSON message sent from the Front-End
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')
        room_name = data.get('room_name')

        print("entra el receive del consumers")
        print(username)
        await self.save_message(username, room_name, message)

        # Send the message to a room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        
    # Receive message from room group
    async def chat_message(self, event):
        print("se envia el mensaje")
        message = event.get('message')
        username = event.get('username')

        # Send message back to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # Store messages sent in a chatroom asynchronously
    
    
    
    async def save_message(self, username, room_name, message):
        print("entra a save message")
        # Get User object from DB by username
        user = await self.get_user(username)

        
        await self.create_message(user, room_name, message)
        # Manage messages receives using a 
        # bot interface
        await self._manage_message(user, room_name, message)
        
    @sync_to_async
    def get_user(self, username):
        
        # Get User object from DB by username
        user = User.objects.get(username=username)
        self.user = user

        return user
    
    @sync_to_async
    def create_message(self, user, room_name, message):
        
        Message.objects.create(user=user,
                               room_name=room_name,
                               message=message)


    async def _manage_message(self, user, room_name, message):
        print("entra a manage message")
        recipient = _BotInterface(user.username, room_name)
        print(recipient)
        await recipient.receive(
        user=user,
        message=message,
        medium=self)

