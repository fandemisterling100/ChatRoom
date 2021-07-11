# Browser-based Chat App  📈 💻
Chatrooms web application with bot assistance to consult share quotes in the market. Implemented using Django, Redis, Channels and RabbitMQ.

## Features ✔️

-  User registration and login.
- Allow users to post messages in a room of their choosing.
- Show the last 50 messages in the chatroom.
- Bot assistance using the command `/stock=stock_code`, where `stock_code` refers to the company symbol.
- Connection to API Stooq to consult the maximum stock quote of the shares.
- Messages ordered by their timestamps.
- Usage of RabbitMQ as message broker to implement a decoupled bot which answer the queries about stock shares posted in the chatrooms.
## Implemented Bonus ➕
- The App allows users to connect to different chat rooms by typing a room name in the index page.
- Handle messages that are not understood.
- Handle exceptions raised within the bot.

## Installation ⚙️
1. Clone repository from `https://github.com/fandemisterling100/ChatRoom.git`
2. Install the packages required from the `ChatRoom/` folder via:

`$ pip install -r requirements.txt`

3.  To use the Redis and RabbitMQ services we will use docker containers (Be sure your docker daemon is running):

    	 `$ sudo apt install docker.io` (If you don't have Docker installed) 

	 `$ sudo dockerd`

	 `$ sudo docker run -p 6379:6379 -d redis:5`

	 `$ sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`


4.   Make migrations and migrate them to create the db.sqlite3 on your project directory (being inside `ChatRoom/` folder):

	 `$ python manage.py makemigrations chatroom`

	 `$ python manage.py migrate`

5. Serve page:

	`$ python manage.py runserver`

6.  Create bot user by clicking on **Register Here** and filling the fields according to the following information:

	```javascript
	USER_DATA = {
		"username": "Bot",
		"email": "bot@email.com",
		"password": "1234" 
		}
	```

7. LogOut

## Usage 🧑‍💻
1. Move to folder `decoupled_bot/` and run the decoupled bot to start to consume from the stock queue:
 `python3 -m bot_package.consumers`
 
2. Return to folder `ChatRoom/` and serve the page (if it was not being served) via: `$ python manage.py runserver`

3. Now you can register on the page your own users and Log them in.
4. To get into a chat room just type a valid room name (alphanumeric value) from the index page (redirected when you log in) and click on **Join**.
5. Start chatting!

## Bot commands
The word **user** is replaced with the username of whom invoked the bot. **STOCK_CODE** corresponds to the company symbol that the user is asking and **value** corresponds to the maximum quote of the shares.

| Command     | Bot Answer |
| --------- | -----:|
| /hi  | Hi user! How are you? |
| /bye     |   See you user! |
| /help      |    Hello user! You can use the command /stock=stock_code to check the value of that stock in the market |
| /stock=stock_code      |   STOCK_CODE quote is $value per share |
| Other words starting with / | sorry user, I did not understand, try /help |


## Additional Info
All the commands were executed from an Ubuntu-20.04 window
##### Python Version: 3.8.5
##### pip Version: 20.0.2
