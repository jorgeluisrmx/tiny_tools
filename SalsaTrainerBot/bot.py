#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
SalsaTrainerBot Main module: handler definition and registration
Copyright (C) 2016  jorgeluisrmx

Contact: jorgeluisrmx@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import telegram  
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from validator import Validator
from salsatrainer import SalsaTrainer


auth = Validator()
trainer = SalsaTrainer('data')

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def load_credentials(fname):
    with open(fname, 'r') as fjson:
        cred = json.load(fjson)
    return cred

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def start(bot, update):  
    """
    Handler for /start command
    """
    
    if auth.valid_user(update):
        if trainer.has_category():
            bot.sendMessage(chat_id=update.message.chat_id, 
            text='To change training category please /stop current one, and /start a new one.')
        else:
            keyb = [[str(i+1)+'. '+item] for i, item in enumerate(trainer.get_categories())]
            reply_markup = telegram.ReplyKeyboardMarkup(keyboard=keyb,
                                            resize_keyboard=True, one_time_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, 
                            text="Welcome!!!, please choose a category to practice:",
                            reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, you're not an authorized user for this bot")

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def stop(bot, update):
    """
    Handler for /stop command
    """
    
    if auth.valid_user(update):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Ok, here ends our training, well done!!!")
        trainer.stop()
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, you're not an authorized user for this bot")

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def msgmngr(bot, update):
    """
    Handler for incomming text messages
    """
    
    selcat = update.message.text.split('. ')[-1].encode('utf8')
    if trainer.has_category():
        bot.sendMessage(chat_id=update.message.chat_id, 
        text='To change training category please /stop current one, and /start a new one.')
    else:
        if trainer.set_category(selcat, update.message.chat_id):
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='{} training begins!!!'.format(selcat),
                            reply_markup=telegram.ReplyKeyboardHide())
            trainer.start()
        else:
            keyb = [[str(i+1)+'. '+item] for i, item in enumerate(trainer.get_categories())]
            reply_markup = telegram.ReplyKeyboardMarkup(keyboard=keyb,
                                            resize_keyboard=True, one_time_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, 
                            text='Invalid category, please select a valid one:',
                            reply_markup=reply_markup)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def main():
    """
    Main function
    """
    # load credentials
    credentials = load_credentials('credentials.json')
    auth.set_data(credentials)
    # create bot updater
    updater = Updater(token=credentials['token'])
    trainer.attach_jobqueue(updater.job_queue)
    dispatcher = updater.dispatcher
    print updater.bot.getMe()

    # handler registration
    dispatcher.add_handler( CommandHandler('start', start) )
    dispatcher.add_handler( CommandHandler('stop', stop) )
    dispatcher.add_handler( MessageHandler([Filters.text], msgmngr) )
        
    # launch bot
    updater.start_polling()
    updater.idle()


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    main()


    

