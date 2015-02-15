#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

import datetime
from lib.common.Regexplate import Regexplate

class TimeTableBuilder:

    def __init__(self, date, config):
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.template = Regexplate(config['Journal']['TIME'])
        self.delim = config['Journal']['DELIM']

    def build(self, timetable):
        maps = [self.time_map(s, s+t) for s,t in timetable if self.at_date(s)]
        return self.delim.join([self.template.substitute(m) for m in maps])

    def at_date(self, ts):
        a = datetime.datetime(self.year, self.month, self.day, 0, 0, 0)
        b = a + datetime.timedelta(1)
        return int(a.timestamp()) <= ts and ts < int(b.timestamp())

    def time_map(self, s, e):
        start = datetime.datetime.fromtimestamp(s)
        end = datetime.datetime.fromtimestamp(e)
        return {'SHOUR': start.hour, 'SMIN': '{:02}'.format(start.minute),
                'EHOUR': end.hour, 'EMIN': '{:02}'.format(end.minute)}

if __name__ == '__main__':
    # コンフィグ
    import configparser
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    ttb = TimeTableBuilder(today, config)
    tt = [
            (int(datetime.datetime(2015, 2, 7, 9, 0, 0).timestamp()), 3600),
            (int(datetime.datetime(2015, 2, 7, 10, 0, 0).timestamp()), 3600),
            ]
    print(ttb.build(tt))
