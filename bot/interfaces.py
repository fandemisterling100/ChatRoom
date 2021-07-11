"""Bot interface to filter messages that correspond to a stock command.
   This class receives messages from chat rooms, checks if they are
   commands, responds if it is not a stock query, and if it is, it uses
   the Producer entity (RabbitMQ) to post the query in a queue that the
   decoupled bot consumes.
"""

from chatroom.models import User
from .entities import QUERY, _Producer, Consumer
from .bot_data import *
import json
import asyncio
import threading


class _BotInterface(_Producer):
    def __init__(self, name, group_name):

        # To get access to 'publish_query' method
        super(_BotInterface, self).__init__()
        self.room_group_name = group_name

    async def receive(self, user, message, medium):
        self.client = user
        self.medium = medium

        # Check if it is a stock command
        is_command = await self.__check_command(message)
        if is_command:
            # Post query on a queue
            self.publish_query(message, self.client.username)
            self.__await_result()
        else:
            # Return to the corresponding chatroom a default answer
            answer = await self.__choose_answer(message, self.client.username)
            if answer: await self.__send_answer(answer)
            return

    @staticmethod
    async def __check_command(message):
        """
            Parameters:
                message (str): Chat message received
            Returns
                (bool): True if message is a stock command
        """
        return True if message.startswith(f"/{QUERY}") else False

    @staticmethod
    async def __choose_answer(message, username):
        """Pick an answer according to default options
        """
        for option in ANSWERS.keys():
            if message.startswith(option):
                return ANSWERS[option].replace("user", username)

        if message.startswith('/'):
            return DEFAULT.replace("user", username)
        return None

    async def __send_answer(self, answer):
        print("Bot tries to send message")
        await self.medium.receive(json.dumps({'message': answer,
                                              'username': USER_DATA.get("username"),
                                              'room_name': self.room_group_name}))

    def __await_result(self):
        print("Threading")
        listen_thread = threading.Thread(
            target=Consumer,
            args=(self, f"BotStocks-{self.client.username}"))
        listen_thread.start()

    def send_stock_quote(self, bot_answer):
        """Sends the bot answer to the chatroom using
           the websocket consumer
        """

        print("Sending bot answer from Chat App...")
        loop = asyncio.new_event_loop()
        loop.run_until_complete(
            self.medium.send(text_data=json.dumps({
            'message': bot_answer,
            'username': "Bot"
        })))
