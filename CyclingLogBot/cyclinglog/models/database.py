#-*- coding:utf-8 -*-

"""
Database class for CyclingLog

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

import sqlite3


class Database(object):
    DB_URI = None           # db URI
    CONN= None              # db connection
    CUR = None              # db cursor


    @classmethod
    def initialize(cls, db_uri):
        """
        Innitialize the connection with the sqlite DB
        """
        if (cls.CONN==None) and (cls.CUR==None):
            cls.DB_URI = db_uri
            # chack same thread false to operate DB from different threads
            cls.CONN = sqlite3.connect(db_uri, check_same_thread=False)
            # enforce foreing key
            cls.CONN.execute("PRAGMA foreign_keys = ON")
            cls.CUR = cls.CONN.cursor()
        else:
            raise DatabaseError("Database has been already initialized. Close it before trying again")


    @classmethod
    def create_db_tables(cls):
        """
        Creates a new CyclingLog SQLITE DB instance
        """
        if cls.CONN:
            # creating stages table
            stages_table = """CREATE TABLE stages (
            	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            	name TEXT NOT NULL UNIQUE
            );"""
            cls.execute(stages_table)

            # creating log table
            activities_table = """CREATE TABLE activities (
            	date TEXT NOT NULL,
            	route TEXT NOT NULL,
            	mod TEXT,
            	stage INTEGER NOT NULL,
            	distance REAL NOT NULL,
            	time_start TEXT NOT NULL,
            	time INTEGER,
            	time_moving INTEGER,
            	speed REAL,
            	speed_moving REAL,
            	speed_max REAL,
            	elev_gain REAL,
            	elev_loss REAL,
            	elev_min REAL,
            	elev_max REAL,
            	cycle INTEGER NOT NULL,
            	toi INTEGER,
            	toi_label TEXT,
            	comments TEXT,
            	gpx_filename TEXT,
            	PRIMARY KEY(date, route),
            	FOREIGN KEY(stage) REFERENCES stages(id)
            );"""
            cls.execute(activities_table)

            # commit changes
            cls.commit()
        else:
            raise DatabaseError("Database has not been initialized")


    @classmethod
    def execute(cls, query, values=None):
        """
        Execute a transaction in the database
        """
        if cls.CONN:
            if values:
                return cls.CUR.execute(query, values)
            return cls.CUR.execute(query)
        else:
            raise DatabaseError("Database has not been initialized")


    @classmethod
    def execute_many(cls, query, value_lst):
        """
        Execute many transactions in the database
        """
        if cls.CONN:
            if not isinstance(value_lst, list):
                raise DatabaseError("value_lst is not a list of tuples")
            cls.CUR.executemany(query, value_lst)
            cls.commit()
        else:
            raise DatabaseError("Database has not been initialized")


    @classmethod
    def commit(cls):
        """
        Commit changes in database
        """
        if cls.CONN:
            cls.CONN.commit()
        else:
            raise DatabaseError("Database has not been initialized")


    @classmethod
    def close(cls):
        """
        Closes database
        """
        if cls.CONN:
            cls.CONN.close()
            cls.CONN, cls.CUR, cls.DB_URI = None, None, None


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class DatabaseError(Exception):
    pass
