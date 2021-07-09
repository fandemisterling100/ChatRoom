from chatroom.models import User
from .entities import QUERY, _Producer
from .bot_data import *
import json
import asyncio, concurrent.futures
from asgiref.sync import sync_to_async

class _BotInterface(_Producer):
    def __init__(self, name, group_name):
        
        # To get access to create_queue method
        super(_BotInterface, self).__init__()
        self.room_group_name = group_name
            
    async def receive(self, user, message, medium):
        """Check if the message received is a 
           special command to call a bot
        """
        self.client = user
        self.medium = medium
        is_command = await self.__check_command(message)
        if is_command:
            self.create_queue(message, self.client.username)
            self.__await_result()
        else:
            answer = await self.__choose_answer(message,self.client.username)
            if answer: await self.__send_answer(answer)
            return
        
    async def __check_command(self, message):
        return True if message.startswith(QUERY) else False
    
    async def __choose_answer(self, message, username):
        """Pick an answer according to default options
        """
        for option in ANSWERS.keys():
            if message.startswith(option):
                return ANSWERS[option].replace("user", username)
            elif message.startswith('/'):
                return DEFAULT.replace("user", username)
            else:
                return None
            
    async def __send_answer(self, answer):
        # await self.medium.send(text_data=json.dumps({
        #     'message': answer,
        #     'username': USER_DATA.get("username")
        # }))
        print("Bot tries to send message")
        await self.medium.receive(json.dumps({'message':answer, 
                                              'username': USER_DATA.get("username"), 
                                              'room_name': self.room_group_name}))
        
        
    # def __await_result(self):
    #     listen_thread = threading.Thread(
    #         target=RedistributionListener,
    #         args=(self, 'redistribution-' + self.client.username))
    #     listen_thread.start()
        