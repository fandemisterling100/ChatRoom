import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message

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
        message = data['message']
        username = data['username']
        room_name = data['room_name']  
        
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
        message = event['message']
        username = event['username']
        
        # Send message back to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    
    # Store messages sent in a chatroom asynchronously
    @sync_to_async
    def save_message(self, username, room_name, message):
        Message.objects.create(username=username,
                               room_name=room_name,
                               message=message)