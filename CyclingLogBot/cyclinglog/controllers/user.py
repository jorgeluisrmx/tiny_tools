#-*- coding:utf-8 -*-

"""
Class that handle all user's file operations, including extract config values from app config directory

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

import json
import os

from appdirs import AppDirs

from cyclinglog.models.database import Database
from cyclinglog.models.stage import Stage


class User(object):
    CONFIG_DIR = AppDirs("CyclingLog", "NatureTech").user_data_dir
    CONFIG_FILE = os.path.join(CONFIG_DIR, 'cylog.conf')
    CONFIG = None
    USER_NAME = None


    @classmethod
    def _create_config_file(cls):
        """
        Creates user_data_dir and config file to store users info in the system
        """
        # creates directory
        if not os.path.exists(cls.CONFIG_DIR):
            os.makedirs(cls.CONFIG_DIR)
        # creates config file
        with open(cls.CONFIG_FILE, 'w') as fout:
            json.dump(cls.CONFIG, fout)


    @classmethod
    def _read_config_file(cls):
        """
        Reads json configuration file if it exist in user_data_dir, else creates it
        """
        if not cls.CONFIG:
            if not os.path.exists(cls.CONFIG_FILE):
                cls.CONFIG = {'users': {}, 'bot': {}, 'elev_api': {}}
                cls._create_config_file()
            else:
                with open(cls.CONFIG_FILE, 'r') as fin:
                    cls.CONFIG = json.load(fin)


    @classmethod
    def _update_config_file(cls):
        """
        Saves the current state of the configuration file. At first checks that CONFIG is not empty, in such case calls _read_config_file
        """
        cls._read_config_file()
        with open(cls.CONFIG_FILE, 'w') as fout:
            json.dump(cls.CONFIG, fout)


    @classmethod
    def set_telegram_bot_config(cls, token):
        cls._read_config_file()
        cls.CONFIG['bot'] = {'token': token}
        cls._update_config_file()


    @classmethod
    def get_telegram_bot_config(cls):
        cls._read_config_file()
        return cls.CONFIG['bot']


    @classmethod
    def set_elevation_api_config(cls, key):
        cls._read_config_file()
        cls.CONFIG['elev_api'] = {'key': key}
        cls._update_config_file()


    @classmethod
    def get_elevation_api_config(cls):
        cls._read_config_file()
        return cls.CONFIG['elev_api']

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @classmethod
    def _create_user_dir(cls):
        # creates the cylog user dir
        if not os.path.exists(cls.main_dir()):
            os.makedirs(cls.main_dir())
        else:
            cls.delete_current_user()
            cls.USER_NAME = None
            raise UserError("user_dir for new user already exists")
        # creates SQLITE db
        cls._initialize_user_db()
        Database.create_db_tables()
        # creates gpxs_dir and gpxs_temp_dir
        os.makedirs(cls.gpx_dir())
        os.makedirs(cls.gpx_tmp_dir())


    @classmethod
    def _validate_user_dir(cls, user_dir_path):
        """
        Returns true if dir contains clog.sqlite and gpx_data/, false otherwise
        """
        if os.path.exists(user_dir_path):
            if not os.path.exists(os.path.join(user_dir_path, "gpx_data")):
                return False
            if not os.path.exists(os.path.join(user_dir_path, "clog.sqlite")):
                return False
            return True
        return False


    @classmethod
    def _initialize_user_db(cls):
        if cls.user_selected():
            Database.close()                    # just in case there is an open instance
            Database.initialize(cls.db_path())   # initialize DB connection


    @classmethod
    def select_user(cls, user_name):
        """
        Select as current user the given user_name if it is valid
        """
        cls._read_config_file()
        if user_name in cls.users():
            cls.USER_NAME = user_name
            if cls._validate_user_dir(cls.main_dir()):
                cls._initialize_user_db()
            else:
                cls.USER_NAME = None
                raise UserError("Non valid content of user log dir")
        else:
            cls.USER_NAME = None
            raise UserError("Invalid username")


    @classmethod
    def users(cls):
        cls._read_config_file()
        if cls.CONFIG:
            return cls.CONFIG['users'].keys()
        return []


    @classmethod
    def user_selected(cls):
        """
        Returns true if user_name != None
        """
        return True if cls.USER_NAME else False


    @classmethod
    def current_user(cls):
        """
        Returns the name of the current user
        """
        if cls.user_selected():
            return cls.USER_NAME
        raise UserError('No user has been selected')


    @classmethod
    def main_dir(cls):
        if cls.user_selected():
            return cls.CONFIG['users'][cls.USER_NAME]
        raise UserError('No user has been selected')

    @classmethod
    def db_path(cls):
        if cls.user_selected():
            return os.path.join(cls.main_dir(), "clog.sqlite")
        raise UserError('No user has been selected')

    @classmethod
    def gpx_dir(cls, filename=None):
        if cls.user_selected():
            if filename:
                return os.path.join(cls.main_dir(), "gpx_data", filename)
            return os.path.join(cls.main_dir(), "gpx_data")
        raise UserError('No user has been selected')

    @classmethod
    def gpx_tmp_dir(cls, filename=None):
        if cls.user_selected():
            if filename:
                return os.path.join(cls.gpx_dir(), "tmp", filename)
            return os.path.join(cls.gpx_dir(), "tmp")
        raise UserError('No user has been selected')


    # @classmethod
    # def save_gpx_tmp(cls, tmp_filename):
    #     pass


    @classmethod
    def save_gpx(cls, tmp_filename, new_filename):
        if cls.user_selected():
            with open(cls.gpx_tmp_dir(tmp_filename), 'r') as f_tmp:
                with open(cls.gpx_dir(new_filename), 'w') as f_new:
                    for line in f_tmp:
                        f_new.write(line)


    @classmethod
    def delete_gpx_tmp(cls, tmp_filename):
        if cls.user_selected():
            os.remove(cls.gpx_tmp_dir(tmp_filename))


    @classmethod
    def delete_gpx(cls, filename):
        if cls.user_selected():
            os.remove(cls.gpx_dir(filename))


    @classmethod
    def create_new_user(cls, user_name, user_dir_path, from_previous=False):
        """
        Creates a new user_name: user_dir_path pair,
        if from_previous == False, creates the CyclingLog
        directory structure and DB, and finally update the config file,
        otherwise user_cylog_dir_path is validated

        NOTE: user_name SHOULD BE Telegram's user_name if bot want to be used by the user
        """
        cls._read_config_file()
        if user_name not in cls.users():
            # validate user_dir_path if from_previous
            if from_previous and (not cls._validate_user_dir(user_dir_path)):
                raise UserError("Non valid user_dir for new user")
            # sets the new user as current user
            cls.USER_NAME = user_name
            # creates a new entry in the config directory
            cls.CONFIG['users'][cls.USER_NAME] = user_dir_path
            if from_previous:
                cls._initialize_user_db()
            else:
                # creates the dir structure and DB requiered by CyclingLog
                cls._create_user_dir()
            # updates the config file
            cls._update_config_file()
        else:
            cls.USER_NAME = None
            raise UserError("User name already registered")


    @classmethod
    def update_user_dir(cls, user_name, user_dir_path):
        """
        Update the user_dir_path info for a given user_name
        """
        cls._read_config_file()
        # validate the content of user_dir_path to conform the CyclingLog needs
        if user_name in cls.users():
            if cls._validate_user_dir(user_dir_path):
                # update user data in config dictionary
                cls.USER_NAME = user_name
                cls.CONFIG['users'][cls.USER_NAME] = user_dir_path
                cls._initialize_user_db()
                cls._update_config_file()
            else:
                cls.USER_NAME = None
                raise UserError("Non valid content of user log dir")
        else:
            raise UserError("User profile does not exist")


    @classmethod
    def delete_current_user(cls):
        """
        Deletes current user from config file, and set user_name to None
        """
        if not cls.user_selected():
            raise UserError("No user selected")
        del cls.CONFIG['users'][cls.USER_NAME]
        cls.USER_NAME = None
        Database.close()
        cls._update_config_file()


    @classmethod
    def delete_user(cls, user_name):
        cls._read_config_file()
        if user_name in cls.users():
            if (not cls.user_selected()) or (cls.USER_NAME != user_name):
                del cls.CONFIG['users'][user_name]
                cls._update_config_file()
            else:
                raise Exception("To delete current user use 'delete_current_user()' method")
        else:
            raise UserError("User '{}' does not exist".format(user_name))


    @classmethod
    def close_user_session(cls):
        if cls.user_selected():
            cls.USER_NAME = None
            Stage.clear()
            Database.close()


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class UserError(Exception):
    pass
