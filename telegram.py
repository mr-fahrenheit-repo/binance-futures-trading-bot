import os 
import telebot
from customized import my_balance_string

# Balance in string format
balance = 'Current balance : {}'.format(my_balance_string())

# Bot API KEY 
bot = telebot.TeleBot(os.getenv('api_key_telegram'))

# Message Handler
@bot.message_handler(commands = ['balance'])
def mybalance(message):
    bot.send_message(message.chat.id, balance)

# Keep running script
bot.infinity_polling()