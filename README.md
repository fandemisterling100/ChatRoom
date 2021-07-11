# Browser-based Chat App  📈 💻
Chatrooms web application with bot assistance to consult share quotes in the market. Implemented using Django, Redis, Channels and RabbitMQ.

**Table of Contents** :tw-1f4cb:

[TOC]

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

## Usage 🧑‍💻
