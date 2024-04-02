## this file is based on version 13.7 of python telegram chatbot
## and version 1.26.18 of urllib3
## chatbot.pyfrom telegram import Update
import os
import telegram
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
# The messageHandler is used for all message update
#import configparser
import logging
#import redis
#from ChatGPT_HKBU import HKBU_ChatGPT
import requests
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient("mongodb+srv://ystsang:daisyyst@cluster0.ia5uqdw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["telegram_chatbot"]  # Specify your database name
collection = db["message_counts"]  # Specify your collection name

#global redis1
def main():
    # Load your token and create an Updater for your Bot
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    #updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    #global redis1
    #redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']))
   
    # You can set this logging module, so you will know when and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    global chatgpt
    #chatgpt = HKBU_ChatGPT(config)
    chatgpt = HKBU_GPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()



def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


def equiped_chatgpt(update, context): 
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Store keyword counts in MongoDB"""
    try:
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        # Find the document corresponding to the keyword
        doc = collection.find_one({"_id": msg})
        if doc:
            # If the document exists, increment the count
            collection.update_one({"_id": msg}, {"$inc": {"count": 1}})
            count = doc["count"] + 1
        else:
            # If the document does not exist, create a new one with count 1
            collection.insert_one({"_id": msg, "count": 1})
            count = 1
        update.message.reply_text(f'You have said {msg} {count} times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

class HKBU_GPT():
    #def __init__(self,config_='./config.ini'):
    def __init__(self,config_='./config.ini'):
        #if type(config_) == str:
        #    self.config = configparser.ConfigParser()
        #    self.config.read(config_)
        #elif type(config_) == configparser.ConfigParser:
        #    self.config = config_
        pass

    def submit(self,message):   
        config = configparser.ConfigParser()
        config.read('config.ini')
        conversation = [{"role": "user", "content": message}]
        #url = (config['CHATGPT']['BASICURL']) + "/deployments/" + (config['CHATGPT']['MODELNAME']) + "/chat/completions/?api-version=" + (config['CHATGPT']['APIVERSION'])
        url = (os.environ['BASICURL']) + "/deployments/" + (os.environ['MODELNAME']) + "/chat/completions/?api-version=" + (os.environ['APIVERSION'])
        #headers = { 'Content-Type': 'application/json', 'api-key': (config['CHATGPT']['ACCESS_TOKEN']) }
        headers = { 'Content-Type': 'application/json', 'api-key': (os.environ['GPT_ACCESS_TOKEN']) }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response

if __name__ == '__main__':
    main()
