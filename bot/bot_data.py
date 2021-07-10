""" Information about answers to specific commands of the bot
    and a default answer when the user tries an unknown command.
    User data for creating the bot user in the DB.
"""

ANSWERS = {'/help': " Hello user! You can use the command /stock=stock_code to check the value of that stock in the market",
           '/hi': "Hi user! How are you?",
           '/bye': "See you user!"}
DEFAULT = "sorry user, I did not understand, try /help"

USER_DATA = {
    "username": "Bot",
    "email": "bot@email.com"
}
