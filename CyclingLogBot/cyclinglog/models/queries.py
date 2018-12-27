#-*- coding:utf-8 -*-

"""
Abstract classes to add query capacity to the Activity class

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

from collections import OrderedDict

from cyclinglog.models.database import Database
from cyclinglog.models.stage import Stage
from cyclinglog.models.tools import seconds2timestring


month_abb= {'01': 'JAN', '02': 'FEB', '03': 'MAR',
            '04': 'APR', '05': 'MAY', '06': 'JUN',
            '07': 'JUL', '08': 'AUG', '09': 'SEP',
            '10': 'OCT', '11': 'NOV', '12': 'DIC'}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def date_formating(date_str):
    """
    Tranforms a string date from YYYY-MM-DD to DD-mmm'YY
    """
    return "{day}-{month}'{year}".format(day=date_str[-2:],
                                         month=month_abb[date_str[5:7]],
                                         year=date_str[2:4])

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def sqlite_query2dict_list(qcur):
    """
    Returns a list of ordered dictionaries containing the query results

    :param qcur: query cursor
    """
    header = [tup[0] for tup in qcur.description]
    query_res = []
    for row in qcur:
        rowd = OrderedDict()
        for key, value in zip(header, row):
            rowd[key] = value
        query_res.append(rowd)
    return query_res

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class ActivityQuery(object):
    """
    Class with Activity related queries as methods
    """

    @classmethod
    def routes(cls):
        """
        Returns a sorted list of the distinct route's names in db
        """
        qcur = Database.execute('SELECT DISTINCT route FROM {} ORDER BY route'.format(cls.TABLE_NAME))
        return [row[0] for row in qcur]


    @classmethod
    def mods(cls):
        """
        Returns a sorted list of the distinct mods in db
        """
        qcur = Database.execute('SELECT DISTINCT mod FROM {} WHERE mod IS NOT NULL ORDER BY mod'.format(cls.TABLE_NAME))
        return [row[0] for row in qcur]


    @classmethod
    def stages(cls):
        """
        Returns a list of the stages in the db
        """
        return Stage.get_names()[::-1]


    @classmethod
    def toi_labels(cls):
        """
        Returns a sorted list of the distinct toi_labels in db
        """
        qcur = Database.execute('SELECT DISTINCT toi_label FROM {} WHERE toi_label IS NOT NULL ORDER BY toi_label'.format(cls.TABLE_NAME))
        return [row[0] for row in qcur]


    @classmethod
    def totals(cls):
        """
        Returns a dictionary containing a summary of all tracks.
        Dict's keys are: 'tracks',                  'distance',
                         'date_from',               'date_to',
                         'time',                    'time_moving',
                         'min_speed_moving',        'max_speed_moving',
                         'avg_speed_moving',        'highest_speed',
                         'elev_gain',               'elev_loss',
                         'elev_min',                'elev_max'
        """
        qcur = Database.execute(
"""SELECT COUNT(*) as tracks,
	sum(distance) as distance,
    min(date) as date_from,
    max(date) as date_to,
	sum(time) as time,
	sum(time_moving) as time_moving,
	min(speed_moving) as min_speed_moving,
	max(speed_moving) as max_speed_moving,
	avg(speed_moving) as avg_speed_moving,
	max(speed_max) as highest_speed,
	sum(elev_gain) as elev_gain,
	sum(elev_loss) as elev_loss,
	min(elev_min) as elev_min,
	max(elev_max) as elev_max
FROM {}""".format(cls.TABLE_NAME))
        summ = sqlite_query2dict_list(qcur)

        # formating time in seconds
        for row in summ:
            row['date_from'] = date_formating(row['date_from'])
            row['date_to'] = date_formating(row['date_to'])
            row['time'] = seconds2timestring(row['time'])
            row['time_moving'] = seconds2timestring(row['time_moving'])

        return summ[0]


    @classmethod
    def rankings(cls):
        pass


    @classmethod
    def summary_by_stage(cls):
        """
        Returns a list of ordered dicts, one item for stage.
        Dict's keys are: 'stage',                       'tracks' (number of),
                         'date_from',                   'date_to',
                         'total_distance',              'total_elev_gain',
                         'total_time',                  'total_time_moving',
                         'not_null_time_tracks',        'not_null_elev_gain_tracks'
        """
        qcur = Database.execute(
"""SELECT name as stage,
          COUNT(route) as tracks,
          min(date) as date_from,
          max(date) as date_to,
          sum(distance) as total_distance,
          sum(elev_gain) as total_elev_gain,
          sum(time) as total_time,
          sum(time_moving) as total_time_moving,
          count(time) as not_null_time_tracks,
          count(elev_gain) as not_null_elev_gain_tracks
FROM {} r1 JOIN {} r2 ON r1.stage = r2.id
GROUP BY stage""".format(cls.TABLE_NAME, Stage.TABLE_NAME))
        summ = sqlite_query2dict_list(qcur)

        # formating time in seconds
        for row in summ:
            row['date_from'] = date_formating(row['date_from'])
            row['date_to'] = date_formating(row['date_to'])
            row['total_time'] = seconds2timestring(row['total_time'])
            row['total_time_moving'] = seconds2timestring(row['total_time_moving'])
            if not row['total_elev_gain']:
                row['total_elev_gain'] = float('nan')

        return summ


    @classmethod
    def summary_by_month(cls):
        """
        Returns a list of ordered dicts, one item for month-year.
        Dict's keys are: 'date',                        'month',
                         'date_from',                   'date_to',
                         'year',                        'tracks' (number of),
                         'total_distance',              'total_elev_gain',
                         'total_time',                  'total_time_moving',
                         'not_null_time_tracks',        'not_null_elev_gain_tracks'
        """
        qcur = Database.execute(
"""SELECT strftime("%m", date) as month,
       min(date) as date_from,
       max(date) as date_to,
	   strftime("%Y", date) as year,
	   COUNT(route) as tracks,
	   sum(distance) as total_distance,
	   sum(elev_gain) as total_elev_gain,
	   sum(time) as total_time,
	   sum(time_moving) as total_time_moving,
	   count(time) as not_null_time_tracks,
	   count(elev_gain) as not_null_elev_gain_tracks
FROM {}
GROUP BY month, year
ORDER BY year DESC, month DESC""".format(cls.TABLE_NAME))
        summ = sqlite_query2dict_list(qcur)

        # formating time in seconds
        for row in summ:
            row['date'] = month_abb[row['month']] + "'" + row['year'][2:]
            row['date_from'] = date_formating(row['date_from'])
            row['date_to'] = date_formating(row['date_to'])
            row['total_time'] = seconds2timestring(row['total_time'])
            row['total_time_moving'] = seconds2timestring(row['total_time_moving'])
            if not row['total_elev_gain']:
                row['total_elev_gain'] = float('nan')

        return summ


    @classmethod
    def summary_by_year(cls):
        """
        Returns a list of ordered dicts, one item for year.
        Dict's keys are: 'year',                        'tracks' (number of),
                         'date_from',                   'date_to',
                         'total_distance',              'total_elev_gain',
                         'total_time',                  'total_time_moving',
                         'not_null_time_tracks',        'not_null_elev_gain_tracks'
        """
        qcur = Database.execute(
"""SELECT strftime("%Y", date) as year,
	   COUNT(route) as tracks,
       min(date) as date_from,
       max(date) as date_to,
	   sum(distance) as total_distance,
	   sum(elev_gain) as total_elev_gain,
	   sum(time) as total_time,
	   sum(time_moving) as total_time_moving,
	   count(time) as not_null_time_tracks,
	   count(elev_gain) as not_null_elev_gain_tracks
FROM {}
GROUP BY year
ORDER BY year DESC""".format(cls.TABLE_NAME))
        summ = sqlite_query2dict_list(qcur)

        # formating time in seconds
        for row in summ:
            row['date_from'] = date_formating(row['date_from'])
            row['date_to'] = date_formating(row['date_to'])
            row['total_time'] = seconds2timestring(row['total_time'])
            row['total_time_moving'] = seconds2timestring(row['total_time_moving'])
            if not row['total_elev_gain']:
                row['total_elev_gain'] = float('nan')

        return summ


    @classmethod
    def summary_by_route(cls):
        """
        Returns a list of ordered dicts, one item for every route.
        Dict's keys are: 'route',                       'tracks' (number of),
                         'date_from',                   'date_to',
                         'total_distance',              'total_elev_gain',
                         'total_time',                  'total_time_moving',
                         'not_null_time_tracks',        'not_null_elev_gain_tracks'
        """
        qcur = Database.execute(
"""SELECT route,
	COUNT(route) as tracks,
    min(date) as date_from,
    max(date) as date_to,
    sum(distance) as total_distance,
    sum(elev_gain) as total_elev_gain,
    sum(time) as total_time,
    sum(time_moving) as total_time_moving,
    count(time) as not_null_time_tracks,
    count(elev_gain) as not_null_elev_gain_tracks
FROM {}
GROUP BY route
ORDER BY route ASC""".format(cls.TABLE_NAME))
        summ = sqlite_query2dict_list(qcur)

        # formating time in seconds
        for row in summ:
            row['date_from'] = date_formating(row['date_from'])
            row['date_to'] = date_formating(row['date_to'])
            row['total_time'] = seconds2timestring(row['total_time'])
            row['total_time_moving'] = seconds2timestring(row['total_time_moving'])
            if not row['total_elev_gain']:
                row['total_elev_gain'] = float('nan')

        return summ
