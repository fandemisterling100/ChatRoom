import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, User
from bot.interfaces import _BotInterface
from bot.bot_data import USER_DATA


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
        # Decode JSON message received
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')
        room_name = data.get('room_name')

        # Send the message to a room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        await self.save_and_check(username, room_name, message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event.get('message')
        username = event.get('username')

        # Send message back to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def save_and_check(self, username, room_name, message):
        user = await self.__get_user(username)

        # Save the message in DB
        await self.__create_message(user, room_name, message)

        # Manage messages received using a bot interface
        await self._manage_message(user, room_name, message)

    @staticmethod
    @sync_to_async
    def __get_user(username):
        # Get User object from DB by username
        user = User.objects.get(username=username)
        return user

    # Store messages sent in a chatroom
    @staticmethod
    @sync_to_async
    def __create_message(user, room_name, message):
        Message.objects.create(user=user,
                               room_name=room_name,
                               message=message)

    # Notify to a bot interface about the new message
    # to check if it is a special command then the
    # decoupledbot awakes
    async def _manage_message(self, user, room_name, message):
        recipient = _BotInterface(user.username, room_name)
        await recipient.receive(
        user=user,
        message=message,
        medium=self)
