#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Validator class implementation for the SalsaTrainerBot
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
__version__ = "1.0.0"
__author__ = "jorgeluisrmx "
__email__ = "jorgeluisrmx@gmail.com"
__copyright__ = "Copyright 2016, jorgeluisrmx"
__license__ = "GNU GPL 3"
__date__ = '18-jun-16'



class Validator(object):
    """
    Validator class. Used to user authentication related issues in the SalsaTrainerBot
    """
    
    def set_data(self, credentials):
        """
        Set necessary data to validate user by Telegram-username
        
        :param credentials: credentials dictionary
        :rtype: None
        """
        self._username = credentials['authuser']
    
    
    def valid_user(self, update):
        """
        Authenticate a user given its id and username
        
        :param update: object containing the incoming message info 
        :type update: python-telegram-bot update object
        :returns: True if updater contain a valid user info, False otherwise
        :rtype: bool
        """
        if self._username == update.message.from_user.username:
            return True
        return False
        
        
