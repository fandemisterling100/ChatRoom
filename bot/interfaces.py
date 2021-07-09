from chatroom.models import User
from .entities import QUERY, _Producer
from .answers import *
import json
import asyncio, concurrent.futures
from asgiref.sync import sync_to_async

class _BotInterface(_Producer):
    def __init__(self, name, group_name):
        
        # To get access to create_queue method
        super(_BotInterface, self).__init__()
        self.room_group_name = group_name
        
        # Find the user who post the message
        self.def_user(name)
    
    @sync_to_async
    def def_user(self, name):
        try:
            self.user = User.objects.get(username=name)
        except User.DoesNotExist:
            print("The user doesn't exist.")
            
    async def receive(self, user, message, medium):
        """Check if the message received is a 
           special command to call a bot
        """
        print("entra al receive del bot")
        self.client = user
        self.medium = medium
        await self.__send_answer("NO FUNCIONA :(","kathe")
        
        is_command = await self.__check_command(message)
        print(f"----------- ES COMANDO: {is_command}")
        # if is_command:
        #     self.create_queue(message, self.client.username)
        #     self.__await_result()
        # else:
        #     answer = self.__choose_answer(message,self.client.username)
        #     self.__send_answer(answer,self.client.username)
        #     return
        
            
    async def __check_command(self, message):
        return True if message.startswith(QUERY) else False
    
    async def __choose_answer(self, message, username):
        """Pick an answer according to default options
        """
        for option in ANSWERS.keys():
            if message.startswith(option):
                return ANSWERS[option].replace("user", username)
            else:
                return DEFAULT.replace("user", username)
            
    async def __send_answer(self, answer, username):
        #self.medium.receive(json.dumps({'message':answer, 'username': username, 'room_name': self.room_group_name}))
        # pool = concurrent.futures.ThreadPoolExecutor()
        # result = pool.submit(asyncio.run, self.medium.receive(json.dumps({'message':answer, 'username': username, 'room_name': self.room_group_name}))).result()
        # print('exiting synchronous_property', result)
        # self.medium.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': answer,
        #         'username': username
        #     }
        # )
        # print("entra a send answer")
        # print(self.medium)
        # print(type(self.medium))
        # await self.medium.send(text_data=json.dumps({
        #     'message': answer,
        #     'username': username
        # }))
        await self.medium.receive(json.dumps({'message':answer, 'username': username, 'room_name': self.room_group_name}))
        
        
    # def __await_result(self):
    #     listen_thread = threading.Thread(
    #         target=RedistributionListener,
    #         args=(self, 'redistribution-' + self.client.username))
    #     listen_thread.start()
        