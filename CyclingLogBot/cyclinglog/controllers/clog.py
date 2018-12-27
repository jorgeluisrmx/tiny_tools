#-*- coding:utf-8 -*-

"""
CyclingLog main controller class

Copyright (c) 2017 Jorge Luis Rodriguez <jorgeluisrmx@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import unicode_literals

from cyclinglog.controllers.user import User
from cyclinglog.controllers.clbot import CLBot


class CyclingLog(object):

    def __init__(self, username=None, init_bot=True):
        """
        Class constructor
        """
        self.bot = None

        if username:
            self.select_user(username)
            # start bot
            if init_bot:
                self.start_bot()


    def start_bot(self):
        """
        Starts the bot if all conditions are satisfied
        """
        # check that user is selected
        if not User.user_selected():
            raise CyclingLog('No user select. Choose one before to launch the bot')
        # check elevation api key exists
        if not User.get_elevation_api_config()['key']:
            raise CyclingLog('ELEVATION API key not registered. Please register one')
        # check for telegram bot TOKEN
        if not User.get_telegram_bot_config()['token']:
            raise CyclingLog('TELEGRAM BOT token not registered. Please register one')
        # start bot
        self.bot = CLBot()


    @classmethod
    def user_list(cls):
        """
        Returns the username's list
        """
        return User.users()


    @classmethod
    def select_user(cls, username):
        """
        Select usernmae if it exists
        """
        User.select_user(username)


    @classmethod
    def create_new_user(cls, usename, user_dir_url):
        """
        Creates a new user
        """
        User.create_new_user(usename, user_dir_url)


    @classmethod
    def delete_user(cls, username=None):
        """
        If not username deletes the current user. Otherwise if it exists, deletes it
        """
        if username:
            User.delete_user(username)
        else:
            User.delete_current_user()


    @classmethod
    def update_user_dir(cls, username, user_dir_url):
        """
        Updates the user_dir_url
        """
        User.update_user_dir(username, user_dir_url)


    @classmethod
    def set_telegram_bot_config(cls, token):
        User.set_telegram_bot_config(token)


    @classmethod
    def set_elevation_api_config(cls, key):
        User.set_elevation_api_config(key)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class CyclingLogError(Exception):
    pass
