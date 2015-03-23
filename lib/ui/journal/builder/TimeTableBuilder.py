#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        maps = [self.time_map(s, s+t) for s, t in timetable if self.at_date(s)]
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
