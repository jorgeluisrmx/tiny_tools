#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
SalsaTrainer class implementation for the SalsaTrainerBot
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

import os
from os.path import isdir, isfile, join
from collections import defaultdict
import random

class SalsaTrainer(object):
    """
    SalsaTrainer class, in charge of trainning session management
    for SalsaTrainerBot
    """
    
    def __init__(self, datadir):
        """
        Constructor
        
        :param datadir: directory where the steps textfile can be found
        :rtype: None
        """
        
        self._datadir = datadir
        self._jobq = None
        self._chatid = None
        self._steps = self.get_data()
        self._cat = None                # chosen category
    
    
    def get_data(self):
        """
        Look for, reads and organize steps lists by category in a dictionary
        
        :returns: Steps dictionary
        ;rtype: Tuple
        """
        # steps files searching
        orgdir = os.getcwd()
        os.chdir('./' + self._datadir)
        file_lst = [join(os.getcwd(), f) for f in os.listdir(os.getcwd()) 
                            if (isfile(join(os.getcwd(), f))) and (not f.endswith('~'))]
        # reset original working directory
        os.chdir(orgdir)
        if not file_lst: raise Exception('No steps files in directory')
        # steps files processing
        steps = defaultdict(list)
        for fname in file_lst:
            with open(fname, 'r') as fin:
                category = fin.readline().lstrip(':').strip('\n')
                for line in fin:
                    steps[category].append(line.strip('\n'))
        if not steps: raise Exception('Nos steps in steps files')
        return steps
    
    
    def attach_jobqueue(self, job_queue):
        """
        Stores a reference to the bot's job_queue
        
        :param: job_queue reference
        :rtype: None
        """
        
        self._jobq = job_queue


    def get_categories(self):
        """
        Return the categories stored in the steps dictionary
        
        :returns: categories list
        :rtype: list
        """
        return self._steps.keys()
    
    
    def set_category(self, cat, chat_id):
        """
        Set the desire category of steps to conduct the training and registers the chat_id
        
        :param cat: id of category to be selected from those in steps dictionary
        :type cat: string
        :param chat_id: id of the target chat
        :returns: True if valid category selected, False otherwise
        :rtype: bool
        """
        
        self._chatid = chat_id
        if cat in self._steps:
            self._cat = cat
            return True
        return False
    
    
    def has_category(self):
        """
        Indicates if a category as been set
        
        :return: True if category has been setted, False otherwise
        :rtype: bool
        """
        
        return True if self._cat else False

    
    def start(self):
        """
        Functions that choose the next step and put the job in the job queue,
        also called from the job when executed to select a new step
        
        :rtype: None
        """
        
        if (not self._cat) or (not self._chatid):
            raise Exception('No chat_id or category when SalsaTrainer.start() called')
        self._jobq.put(self.step_generator(),
                        interval=7, repeat=False, next_t=7, prevent_autostart=False)
    
    
    def step_generator(self):
        """
        Method to generate a single argument function to be called by the job queue
        but need to contain info stored on the data members of the SalsaTrainer class
        
        :returns: job function for the job queue
        :rtype: function
        """
        
        # random choose of next step
        random.shuffle(self._steps[self._cat])
        ntep = random.choice(self._steps[self._cat])
        # next_step funtion is a job-like function for the job queue
        # can only receive one argument, a bot
        def next_step(bot):
            bot.sendMessage(chat_id=self._chatid, text=ntep)
            # re-run the cycle calling SalsaTrainer.start() to register the next step
            self.start()
        # return the next_step function
        return next_step
    
    def stop(self):
        """
        Stops the job_queue
        
        :rtype: None
        """
        
        self._cat = None
        if self._jobq: self._jobq.stop()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    mtrainer = SalsaTrainer('data')
#    print mtrainer._cat
#    print mtrainer.get_categories()
    print mtrainer._steps['Combinaciones']
    random.shuffle(mtrainer._steps['Combinaciones'])
    print mtrainer._steps['Combinaciones']
    print
    print random.choice(mtrainer._steps['Combinaciones'])
    
