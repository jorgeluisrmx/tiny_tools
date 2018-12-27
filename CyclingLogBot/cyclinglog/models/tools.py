#-*- coding:utf-8 -*-

"""
Contains tools for models of CyclingLog

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

import re
from datetime import datetime, timedelta


def time2seconds(tm):
    """
    Takes a time variable and returns the number of seconds represented by it
    """
    return tm.hour*3600 + tm.minute*60 + tm.second

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

time_pattern = re.compile("^([0-9]+):([0-9][0-9]):([0-9][0-9])$")

def timestring2seconds(ts):
    """
    Takes a string, determine if it match the time pattern, if True extract time info and convert it to seconds, else an Exception is raised
    """
    if time_pattern.match(ts):
        hours, minutes, seconds = [int(tstr) for tstr in time_pattern.findall(ts)[0]]
        return hours*3600 + minutes*60 + seconds
    raise Exception("{} does not match time pattern".format(ts))


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def seconds2time(my_seconds):
    """
    Takes my_seconds in seconds and returns it as a time variable
    """
    return (datetime(1970,1,1) + timedelta(seconds=my_seconds)).time()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def seconds2timestring(secs):
    """
    Takes secs in seconds and returns its time string representation
    """
    if not secs:
        secs = 0
    return "{:02d}:{:02d}:{:02d}".format(secs/3600, (secs/60)%60, secs%60)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def ms2kmh(ms):
    """
    Transforme a measure of velocity in m/s to km/h
    """
    # ms * 60**2 / 1000.0
    return 3.6 * ms

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def chunks(l, n):
    """Given a list l, yields successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        if i+n > len(l):
            yield l[i:]
        else:
            yield l[i: i + n]
