# Import libraries
import os 
import requests

# Telegram API
telegram_api = os.getenv('api_key_telegram')
telegram_chat_id = os.getenv('chat_id_telegram')

# Function for Telegram Notification
def telegram_send(chat):
  bot_token = telegram_api
  bot_chat_id = telegram_chat_id
  chat_message = 'https://api.telegram.org./bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id +'&text=' + chat
  response = requests.get(chat_message)
  return response.json()