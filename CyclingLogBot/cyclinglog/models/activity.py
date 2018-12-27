#-*- coding:utf-8 -*-

"""
Models a cycling activity, and makes the bridge between OOP and SQL databse tuples

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

import os
from datetime import date as datetime_date
from datetime import datetime, time, timedelta
from hashlib import sha1

import googlemaps
import gpxpy

from cyclinglog.controllers.user import User
from cyclinglog.models.database import Database
from cyclinglog.models.queries import ActivityQuery
from cyclinglog.models.stage import Stage
from cyclinglog.models.tools import (chunks, ms2kmh, seconds2timestring,
                                     time2seconds, timestring2seconds)


# - - - - - - - - - - - - - - - - - - - - - - - -
# Data validation functions: parameter SPECIFIC
# - - - - - - - - - - - - - - - - - - - - - - - -

def validate_date(value):
    if isinstance(value, datetime_date):
        return value
    elif isinstance(value, str) or isinstance(value, unicode):
        return datetime.strptime(value, '%Y-%m-%d').date()
    else:
        raise InvalidTypeError("Invalid type for date")


def validate_stage(value):
    if (not (isinstance(value, str) or isinstance(value, unicode))) or (value not in Stage.get_names()):
        raise InvalidTypeError("Stage {} not in stages. Please register it first".format(value))
    return Stage.get_id(value)


def validate_time_start(value):
    if isinstance(value, time):
        return value
    elif isinstance(value, str) or isinstance(value, unicode):
        return datetime.strptime(value, '%H:%M:%S').time()
    else:
        raise InvalidTypeError("Invalid type for date")


def validate_cycle(value):
    if isinstance(value, bool):
        return int(value)
    elif isinstance(value, int):
        return value
    elif isinstance(value, str) or isinstance(value, unicode):
        if value=='False' or value=='false' or value=='0':
            return 0
        return 1
    else:
        raise InvalidTypeError("Non valid type for cycle")


def validate_time_seconds(value):
    """
    Takes value and validate it as a time to be represented in seconds or throws an exception
    """
    if isinstance(value, int) and (value > 0):
        return value
    elif isinstance(value, time):
        return time2seconds(value)
    elif isinstance(value, str) or isinstance(value, unicode):
        try:
            return timestring2seconds(value)
        except Exception as e:
            raise InvalidTypeError(str(e))
    else:
        raise InvalidTypeError("Invalid type for time")

# - - - - - - - - - - - - - - - - - - - - -
# Data validation functions: parameter TYPE
# - - - - - - - - - - - - - - - - - - - - -

def validate_string(value):
    if isinstance(value, str) or isinstance(value, unicode):
        if value=="":
            return None
        return value
    else:
        raise InvalidTypeError("Invalid type, string was expected")


def validate_float(value):
    if isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, str) or isinstance(value, unicode):
        try:
            return float(value)
        except:
            raise InvalidTypeError("Invalid format, float was expected")
    else:
        raise InvalidTypeError("Invalid type, float was expected")

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class Activity(ActivityQuery):
    TABLE_NAME = 'activities'
    FIELDS = ['date', 'route', 'mod', 'stage', 'distance', 'time_start', 'time', 'time_moving', 'speed', 'speed_moving', 'speed_max', 'elev_gain', 'elev_loss', 'elev_min', 'elev_max', 'cycle', 'toi', 'toi_label', 'comments', 'gpx_filename']


    def __init__(self, date, route, stage, distance, time_start, cycle, mod=None, time=None, time_moving=None, speed=None, speed_moving=None, speed_max=None, elev_gain=None, elev_loss=None, elev_min=None, elev_max=None, toi=None, toi_label=None, comments=None, gpx_filename=None):
        """
        Class Constructor

        :param date: date in format aaaa-mm-dd
        :type date: string
        :param route: route name
        :type route: string
        :param mod: name modifier as: recreational, partial, modified(v2.0)
        :type mod: string
        :param stage: stage name but as id number comming from db
        :type stage: int
        :param distance: distance in kilometers
        :type distance: float
        :param time_start: start time in format HH:MM:SS
        :type time_start: string
        :param time: elapsed time in seconds
        :type time: int
        :param time_moving: moving time in seconds
        :type time_moving: int
        :param speed: mean speed km/h -> distance/time
        :type speed: float
        :param speed_moving: moving speed in km/h -> distance/time_moving
        :type speed_moving: float
        :param speed_max: max speed in km/h
        :type speed_max: float
        :param elev_gain: elevation gain in meters
        :type elev_gain: float
        :param elev_loss: elevation loss in meters
        :type elev_loss: float
        :param elev_min: min elevation of the route in meters
        :type elev_min: float
        :param elev_max: max elevation of the route in meters
        :type elev_max: float
        :param cycle: is a cyclical route? as 0|1 comming from DB
        :type cycle: int
        :param toi: time of interest in seconds
        :type toi: int
        :param toi_label: time of interest
        :type toi_label: string
        :param comments: additional comments
        :type comments: string
        :param gpx_filename: gpx file name relative to gpx_date dir (user.gpxs_dir)
        :type gpx_filename: string

        Arguments that has to be casted:
                            from        to              note
            * date          string      date
            * stage         int         string          Stage.get_name()
            * time_start    string      time
            * cycle         int         bool            bool()

        """
        self._update = {}
        self._date = datetime.strptime(date, '%Y-%m-%d').date()
        self._route = route
        self._mod = mod
        self._stage = stage
        self._distance = distance
        self._time_start = datetime.strptime(time_start, '%H:%M:%S').time()
        self._time = int(time) if time else time
        self._time_moving = int(time_moving) if time_moving else time_moving
        self._speed = speed
        self._speed_moving = speed_moving
        self._speed_max = speed_max
        self._elev_gain = elev_gain
        self._elev_loss = elev_loss
        self._elev_min = elev_min
        self._elev_max =  elev_max
        self._cycle = cycle
        self._toi = toi
        self._toi_label = toi_label
        self._comments = comments
        self._gpx_filename = gpx_filename

    # - - - -
    # Getters
    # - - - -

    @property
    def date(self):
        return self._date

    @property
    def route(self):
        return self._route

    @property
    def mod(self):
        return self._mod

    @property
    def stage(self):
        return Stage.get_name(self._stage)

    @property
    def distance(self):
        return self._distance

    @property
    def time_start(self):
        return self._time_start

    @property
    def time(self):
        if self._time:
            return seconds2timestring(self._time)
        return self._time

    @property
    def time_moving(self):
        if self._time_moving:
            return seconds2timestring(self._time_moving)
        return self._time_moving

    @property
    def speed(self):
        return self._speed

    @property
    def speed_moving(self):
        return self._speed_moving

    @property
    def speed_max(self):
        return self._speed_max

    @property
    def elev_gain(self):
        return self._elev_gain

    @property
    def elev_loss(self):
        return self._elev_loss

    @property
    def elev_min(self):
        return self._elev_min

    @property
    def elev_max(self):
        return self._elev_max

    @property
    def cycle(self):
        return bool(self._cycle)

    @property
    def toi(self):
        if self._toi:
            return seconds2timestring(self._toi)
        return self._toi

    @property
    def toi_label(self):
        return self._toi_label

    @property
    def comments(self):
        return self._comments

    @property
    def gpx_filename(self):
        return self._gpx_filename

    # - - - -
    # Setters
    # - - - -

    @date.setter
    def date(self, value):
        # date cannot be changed once it is assiged by DB in a base Activity
        raise ActivityError("Activity's date cannot be reassigned")

    @route.setter
    def route(self, value):
        # route cannot be changed once it is assiged by DB in a base Activity
        raise ActivityError("Activity's route cannot be reassigned")

    @mod.setter
    def mod(self, value):
        self._mod = self._validate_assign_update('mod', value, self._mod,
                                                 validate_string)

    @stage.setter
    def stage(self, value):
        self._stage = self._validate_assign_update('stage', value, self._stage,
                                                    validate_stage)

    @distance.setter
    def distance(self, value):
        self._distance = self._validate_assign_update('distance', value,
                                                      self._distance,
                                                      validate_float)

    @time_start.setter
    def time_start(self, value):
        self._time_start = self._validate_assign_update('time_start', value,
                                                        self._time_start,
                                                        validate_time_start)

    @time.setter
    def time(self, value):
        self._time = self._validate_assign_update('time', value, self._time,
                                                  validate_time_seconds)

    @time_moving.setter
    def time_moving(self, value):
        self._time_moving = self._validate_assign_update('time_moving', value,
                                                         self._time_moving,
                                                         validate_time_seconds)

    @speed.setter
    def speed(self, value):
        self._speed = self._validate_assign_update('speed', value, self._speed,
                                                   validate_float)

    @speed_moving.setter
    def speed_moving(self, value):
        self._speed_moving = self._validate_assign_update('speed_moving', value,
                                                          self._speed_moving,
                                                          validate_float)

    @speed_max.setter
    def speed_max(self, value):
        self._speed_max = self._validate_assign_update('speed_max', value,
                                                       self._speed_max,
                                                       validate_float)

    @elev_gain.setter
    def elev_gain(self, value):
        self._elev_gain = self._validate_assign_update('elev_gain', value,
                                                       self._elev_gain,
                                                       validate_float)

    @elev_loss.setter
    def elev_loss(self, value):
        self._elev_loss = self._validate_assign_update('elev_loss', value,
                                                       self._elev_loss,
                                                       validate_float)

    @elev_min.setter
    def elev_min(self, value):
        self._elev_min = self._validate_assign_update('elev_min', value,
                                                       self._elev_min,
                                                       validate_float)

    @elev_max.setter
    def elev_max(self, value):
        self._elev_max = self._validate_assign_update('elev_max', value,
                                                       self._elev_max,
                                                       validate_float)

    @cycle.setter
    def cycle(self, value):
        self._cycle = self._validate_assign_update('cycle', value, self._cycle,
                                                    validate_cycle)

    @toi.setter
    def toi(self, value):
        self._toi = self._validate_assign_update('toi', value, self._toi,
                                                 validate_time_seconds)

    @toi_label.setter
    def toi_label(self, value):
        self._toi_label = self._validate_assign_update('toi_label', value,
                                                       self._toi_label,
                                                       validate_string)

    @comments.setter
    def comments(self, value):
        self._comments = self._validate_assign_update('comments', value,
                                                       self._comments,
                                                       validate_string)

    @gpx_filename.setter
    def gpx_filename(self, value):
        self._gpx_filename = self._validate_assign_update('gpx_filename', value,
                                                          self._gpx_filename,
                                                          validate_string)


    def _validate_assign_update(self, param_name, value, actual_value, validate_function):
        """
        Takes value, validate it with the validation_function, if not valid throws a InvalidTypeError. If it is valid and different from actual_value, adds it to the _update dictionary under param_name and returns it
        """
        nval = validate_function(value)
        if nval != actual_value:
            self._update[param_name] = nval
        return nval


    def __repr__(self):
        """
        Returns the string representation of the class instance
        """
        if self.time:
            return "{}({}, {}): {}km @ {} in {}".format(type(self).__name__, self.date, self.route, self.distance, self.time_start, self.time)
        return "{}({}, {}): {}km @ {}".format(type(self).__name__, self.date, self.route, self.distance, self.time_start)


    def get_by_name(self, attr_name):
        """
        Get an attribute by its name
        """
        if attr_name in self.FIELDS:
            return getattr(self, attr_name)


    def set_by_name(self, attr_name, value):
        """
        Set the value of an attribute by its name
        """
        if attr_name in self.FIELDS:
            setattr(self, attr_name, value)


    def update(self, **kwargs):
        """
        Updates activity register in DB with the provided data
        """
        if self._update:
            insert_query = []
            for key, value in self._update.items():
                if isinstance(value, str):
                    insert_query.append("{}='{}'".format(key, value))
                else:
                    insert_query.append("{}={}".format(key, value))

            q_header = "UPDATE {} SET ".format(self.TABLE_NAME)
            q_tail = " WHERE date='{}' AND route='{}'".format(self.date, self.route)
            query = q_header + ", ".join(insert_query) + q_tail
            Database.execute(query)
            Database.commit()
            self._update = {}


    def save(self):
        """
        Saves activity as a new record
        """
        # check for minimum data required to create the record
        if (not self._date) or (not self._route) or (self._route=='') or (self._stage==None) or (not self._distance) or (not self._time_start) or (self._cycle==None):
            raise ActivityError("Activity does not contains minimum data required to be registered")
        # insert the record in db
        query = 'INSERT INTO {}({}) VALUES ({})'.format(self.TABLE_NAME, ','.join(self.FIELDS), ','.join(["?"]*len(self.FIELDS)))
        # stage is tranformated into int -> Stage.get_id()
        # cycle is tranformated into int -> int(cycle)
        values = (str(self._date), self._route, self._mod, self._stage, self._distance, str(self._time_start), self._time, self._time_moving, self._speed, self._speed_moving, self._speed_max, self._elev_gain, self._elev_loss, self._elev_min, self._elev_max, self._cycle, self._toi, self._toi_label, self._comments, self._gpx_filename)
        Database.execute(query, values)
        Database.commit()
        self._update = {}


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class ManualActivity(Activity):
    """
    Class that manages the creation of manual activities: those that only consists on date, route, mod, distance, time_start, time, stage, cycle, toi, toi_label, comments
    """

    def __init__(self):
        # prepare date and time_start values
        today_dt = datetime.today()
        ttoday = (today_dt - timedelta(hours=2, minutes=today_dt.minute, seconds=today_dt.second, microseconds=today_dt.microsecond)).time()
        # initialize class attributes
        super(ManualActivity, self).__init__(date=str(today_dt.date()),
                time_start=str(ttoday), route=None, stage=1, distance=None, cycle=True)
        # saved marker
        self._saved = False
        # list of requiered attributes to complete ManualActivity info
        self._required = ['route', 'distance']
        # list of optional attributes to complement ManualActivity info
        self._optional = ['date', 'time_start', 'time', 'mod', 'cycle', 'stage', 'toi', 'toi_label', 'comments']


    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, value):
        pass

    @Activity.date.setter
    def date(self, value):
        if not self.saved:
            self._date = self._validate_assign_update('date', value, self._date,
                                                      validate_date)
        else:
            raise ActivityError("Activity's date cannot be modified after saved")

    @Activity.route.setter
    def route(self, value):
        if not self.saved:
            self._route = self._validate_assign_update('route', value,
                                                        self._route,
                                                        validate_string)
        else:
            raise ActivityError("Activity's route cannot be modified after saved")


    def current_state(self):
        """
        Returns a string representation of the current state of the activity
        """
        curr_state = []
        for attr in ['date', 'route', 'mod', 'time_start', 'time', 'distance', 'cycle', 'stage', 'toi', 'toi_label', 'comments']:
            if self.get_by_name(attr)!=None:
                curr_state.append("{}: {}".format(attr, self.get_by_name(attr)))
        return "\n".join(curr_state)


    def requiered_attrs(self):
        """
        Returns the list of required attributes to complete ManualActivity info
        """
        return self._required


    def optional_attrs(self):
        """
        Returns the list of optional attroibutes to complement the ManualActivity info
        """
        return self._optional


    def ready(self):
        """
        Returns True if _required list is empty
        """
        return not self._required


    def set_by_name(self, attr_name, value):
        """
        Set the value of an attribute by its name and modify _reuired list if necessary
        """
        if (attr_name in self._required) or (attr_name in self._optional):
            setattr(self, attr_name, value)
            if attr_name in self._required:
                self._required.remove(attr_name)
                self._optional.append(attr_name)
        else:
            if self.saved:
                raise ActivityError("{} is not settable in SAVED {} objects".format(attr_name, type(self).__name__))
            else:
                raise ActivityError("{} is not settable in {} objects".format(attr_name, type(self).__name__))


    def save(self):
        """
        Saves activity as a new record
        """
        if self.ready() and (not self.saved):
            super(ManualActivity, self).save()
            self._saved = True
            self._optional.remove('date')
            self._optional.remove('route')
        else:
            if self.saved:
                raise ActivityError("Activity has beed already saved")
            else:
                raise ActivityError("Activity cannot be saved. There's still required attributes to be setted")


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class GpxActivity(Activity):
    """
    Class that manages the creation af activities from a gpx file
    """

    def __init__(self, gpx_filepath):
        """
        Class constructor
        """
        self._gpx_tmp_filename = gpx_filepath
        # checking that gpx tmp file exists
        if not os.path.exists(User.gpx_tmp_dir(self._gpx_tmp_filename)):
            raise ActivityError('Input file does not exist [{}]'.format(User.gpx_tmp_dir(self._gpx_tmp_filename)))
        # check for elevation api key exists
        if not User.get_elevation_api_config():
            raise ActivityError('Please set elevation API config before trying to create GpxActivity')
        # extract imfo from gpx file
        gpx_date = self._gpx_process()
        super(GpxActivity, self).__init__(**gpx_date)
        # saved marker
        self._saved = False
        # list of requiered attributes to complete ManualActivity info
        self._extra_info = ['mod', 'toi', 'toi_label', 'comments']
        # list of optional attributes to complement ManualActivity info
        self._settable_attrs = ['date', 'route', 'stage', 'distance', 'time_start', 'time', 'time_moving', 'speed', 'speed_moving', 'speed_max', 'elev_gain', 'elev_loss', 'elev_min', 'elev_max', 'cycle']


    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, value):
        pass

    @Activity.date.setter
    def date(self, value):
        if not self.saved:
            self._date = self._validate_assign_update('date', value, self._date,
                                                      validate_date)
        else:
            raise ActivityError("Activity's date cannot be modified after saved")

    @Activity.route.setter
    def route(self, value):
        if not self.saved:
            self._route = self._validate_assign_update('route', value,
                                                        self._route,
                                                        validate_string)
        else:
            raise ActivityError("Activity's route cannot be modified after saved")


    def _gpx_process(self):
        """
        Process activity gpx file exctracting: date, route, distance, time_start, time, time_moving, speed, speed_moving, speed_max, elev_gain, elev_loss, elev_min, elev_max and stores them, as well as a new name for the gpx file, in a dictionary that returns
        """
        # creating the gpx_date dictionary
        gpx_data = {}
        # initialize elevation API client
        gmaps = googlemaps.Client(User.get_elevation_api_config()['key'])

        # gpx file parsing
        with open(User.gpx_tmp_dir(self._gpx_tmp_filename), 'r') as fin:
            gpx = gpxpy.parse(fin)
        # getting track points
        gpx_points = []
        for track in gpx.tracks:
            for seg in track.segments:
                gpx_points.extend(seg.points)
        # creating lat, lon tuples for elevation request
        lat_lot_tup = [(p.latitude, p.longitude) for p in gpx_points]
        # getting elevation por each point
        elev_data = []
        for chunk in chunks(lat_lot_tup, 500):
            elev_data.extend(gmaps.elevation(chunk))
        # adding new elevation to points and creating a single segment
        segment = gpxpy.gpx.GPXTrackSegment()
        for point, elev in zip(gpx_points, elev_data):
            new_point = gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude,
                                                elevation=elev['elevation'],
                                                time=point.time)
            segment.points.append(new_point)
        # creating a new gpx objects with the elevation-corrected points
        gpx2 = gpxpy.gpx.GPX()
        gpx2_track = gpxpy.gpx.GPXTrack()
        gpx2_track.segments.append(segment)
        gpx2.tracks.append(gpx2_track)
        gpx2.name = gpx.name

        # filling the data dictionary
        gpx_data['date'] = str(gpx2.get_time_bounds().start_time.date())
        gpx_data['route'] = gpx2.name
        gpx_data['stage'] = 1            # as preliminary value
        gpx_data['distance'] = round(gpx2.length_3d()/1000.0, 2)
        gpx_data['time_start'] = str(gpx2.get_time_bounds().start_time.time())
        gpx_data['time'] = gpx2.get_duration()
        gpx_data['time_moving'] = gpx2.get_moving_data().moving_time
        gpx_data['speed'] = round(ms2kmh(gpx2.length_3d() / gpx2.get_duration()), 2)
        gpx_data['speed_moving'] = round(ms2kmh(gpx2.length_3d() / gpx2.get_moving_data().moving_time), 2)
        gpx_data['speed_max'] = round(ms2kmh(gpx2.get_moving_data().max_speed), 2)
        gpx_data['elev_gain'] = round(gpx2.get_uphill_downhill().uphill, 2)
        gpx_data['elev_loss'] = round(gpx2.get_uphill_downhill().downhill, 2)
        gpx_data['elev_min'] = round(gpx2.get_elevation_extremes().minimum, 2)
        gpx_data['elev_max'] = round(gpx2.get_elevation_extremes().maximum, 2)
        gpx_data['cycle'] = True        # as preliminary value
        gpx_data['gpx_filename'] = sha1(str(gpx_data['date']) + gpx_data['route'] + str(gpx_data['distance']) + str(gpx_data['time_start'])).hexdigest() + ".gpx"

        return gpx_data


    def current_state(self):
        """
        Returns a string representation of the current state of the activity
        """
        curr_state = []
        for attr in self.FIELDS:
            if self.get_by_name(attr)!=None:
                curr_state.append("{}: {}".format(attr, self.get_by_name(attr)))
        return "\n".join(curr_state)


    def extra_info(self):
        """
        Returns the list of extra_info attributes to complement the Activity data
        """
        return self._extra_info


    def settable_attrs(self):
        """
        Returns the list of setabble attributes of the activity
        """
        return self._settable_attrs


    def set_by_name(self, attr_name, value):
        """
        Set the value of an attribute by its name and modify extra_info list if necessary
        """
        if (attr_name in self._extra_info) or (attr_name in self._settable_attrs):
            setattr(self, attr_name, value)
            if attr_name in self._extra_info:
                self._extra_info.remove(attr_name)
                self._settable_attrs.append(attr_name)
        else:
            if self.saved:
                raise ActivityError("{} if not settable in SAVED {} objects".format(attr_name, type(self).__name__))
            else:
                raise ActivityError("{} if not settable in {} objects".format(attr_name, type(self).__name__))


    def save(self):
        """
        Saves activity as a new record
        """
        if not self.saved:
            super(GpxActivity, self).save()
            self._saved = True
            self._settable_attrs.remove('date')
            self._settable_attrs.remove('route')
            # saving gpx file and remove gpx_tmp_file
            User.save_gpx(self._gpx_tmp_filename, self.gpx_filename)
            User.delete_gpx_tmp(self._gpx_tmp_filename)
        else:
            raise ActivityError("Activity has beed already saved")


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class ActivityError(Exception):
    pass

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class InvalidTypeError(Exception):
    pass
