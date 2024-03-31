## this file is based on version 13.7 of python telegram chatbot
## and version 1.26.18 of urllib3
## chatbot.py
import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters
# The messageHandler is used for all message update
#import configparser
import logging

#import subprocess
#import redis_Server
#subprocess.Popen([redis_server.REDIS_SERVER_PATH])

#from gptbot import HKBU_GPT

import requests

def main():
    # Load your token and create an Updater for your Bot
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    #updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(config['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module,
    # so you will know when and why things so not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    # register a dispatcher to handle message: 
    # here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)
    global chatgpt
    #chatgpt = HKBU_ChatGPT(config)
    chatgpt = HKBU_GPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)    
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
        conversation = [{"role": "user", "content": message}]
        #url = (self.config['CHATGPT']['BASICURL']) + "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT']['APIVERSION'])
        url = (config['BASICURL']) + "/deployments/" + (config['MODELNAME']) + "/chat/completions/?api-version=" + (config['APIVERSION'])
        #headers = { 'Content-Type': 'application/json', 'api-key': (self.config['CHATGPT']['ACCESS_TOKEN']) }
        headers = { 'Content-Type': 'application/json', 'api-key': (config['GPT_ACCESS_TOKEN']) }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response

if __name__ == '__main__':
    main()