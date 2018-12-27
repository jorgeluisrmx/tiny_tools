#-*- coding:utf-8 -*-

"""
Stage class for CyclingLog

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
from cyclinglog.models.database import Database


class Stage(object):
    TABLE_NAME = 'stages'
    FIELDS = ['name']
    STAGES = {}

    @classmethod
    def _load_stages(cls):
        """
        Load stages from database and save them in STAGES dictionary
        """
        cls.STAGES = {row[0]: row[1] for row in Database.execute('SELECT * FROM {}'.format(cls.TABLE_NAME))}


    @classmethod
    def add_stage(cls, name):
        """
        Add a new stage name to 'stages' table in DB. Namehas to be unique
        """
        if not cls.STAGES:
            cls._load_stages()
        if name not in cls.STAGES.values():
            query = 'INSERT INTO {}({}) VALUES ({})'.format(cls.TABLE_NAME, ','.join(cls.FIELDS), ','.join(["?"]*len(cls.FIELDS)))
            Database.execute(query, (name,))
            Database.commit()
            cls._load_stages()
        else:
            raise StageError('Stage {} already exists'.format(name))


    @classmethod
    def change_stage_name(cls, name, new_name):
        """
        Change the name fiel of the desired stage by new_name
        """
        if not cls.STAGES:
            cls._load_stages()
        # check if name stage exists
        if name not in cls.STAGES.values():
            raise StageError('Stage {} does not exists'.format(name))
        # makes the change
        if new_name not in cls.STAGES.values():
            query = "UPDATE {} SET name='{}' WHERE id={}".format(cls.TABLE_NAME, new_name, Stage.get_id(name))
            Database.execute(query)
            Database.commit()
            cls._load_stages()
        else:
            raise StageError('Stage {} already exists'.format(new_name))


    @classmethod
    def get_name(cls, _id):
        """
        Returns the name of the stage with id=_id or None if not exist
        """
        if not cls.STAGES:
            cls._load_stages()
        if _id in cls.STAGES:
            return cls.STAGES[_id]
        return None


    @classmethod
    def get_id(cls, _name):
        """
        Returns the id of the stage with name=_name or None if not exist
        """
        if not cls.STAGES:
            cls._load_stages()
        if _name in cls.STAGES.values():
            for key in cls.STAGES:
                if cls.STAGES[key]==_name:
                    return key
        return None


    @classmethod
    def get_names(cls):
        """
        Returns the list of all the names of stages
        """
        if not cls.STAGES:
            cls._load_stages()
        return cls.STAGES.values()


    @classmethod
    def clear(cls):
        cls.STAGES = {}


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class StageError(Exception):
    pass
