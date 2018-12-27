#!/usr/bin/env python
#-*- coding:utf-8 -*-

#  AlsavolumeBot: controls output volume in Ubuntu from telegram
#   
#  Copyright 2016 Jorge Luis Rodriguez <jorgeluisrmx@gmail.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import telegram  
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import alsaaudio
import os
import json



class AlsaVolumeController(object):
    
    def __init__(self, credentials_file):
        # loading info
        credentials = self.load_credentials(credentials_file)
        self.name = credentials['name']
        self.username = credentials['username']
        self.token = credentials['token']
        self.admin = credentials['admin']
        self.audio = alsaaudio.Mixer()
    
        # setting bot
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        # handler registration
        self.dispatcher.add_handler( CommandHandler('start', self.start) )
        self.dispatcher.add_handler( MessageHandler([Filters.text], self.set_vol) )
            
        # launch bot
        self.updater.start_polling()
        self.updater.idle()
    
    
    @staticmethod
    def load_credentials(fname):
        print fname
        file_name = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), fname))
        print file_name
        with open(file_name, 'r') as fjson:
            cred = json.load(fjson)
        return cred
    
    
    def authorized(self, update):
        return update.message.from_user.username == self.admin
    
    
    @staticmethod
    def vol_level(text):
        try:
            level = abs(int(text))
        except:
            return None
        if not (0 <= level <= 100):
            return None
        return level
    
    
    def start(self, bot, update):
        if self.authorized(update):
            bot.sendMessage(chat_id=update.message.chat_id, text="I'm online")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, you're not authorized to give me orders")


    def set_vol(self, bot, update):
        if self.authorized(update):
            level = self.vol_level(update.message.text)
            if level:
                self.audio.setvolume(level) 
                bot.sendMessage(chat_id=update.message.chat_id, text="Volume set to {}".format(level))
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text="Invalid input, should be 1-100")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, you're not authorized to give me orders")

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    bot_ctrllr = AlsaVolumeController('credentials.json')


    
