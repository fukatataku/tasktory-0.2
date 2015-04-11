#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from lib.common.Regexplate import Regexplate
from lib.log.Logger import Logger


class TimeTableBuilder(Logger):

    def __init__(self, date, config):
        t00 = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        t24 = self.t00 + datetime.timedelta(1)
        self.t00 = int(t00.timestamp())
        self.t24 = int(t24.timestamp())
        self.template = Regexplate(config['Journal']['TIME'])
        self.delim = config['Journal']['DELIM']
        super().__init__()

    @Logger.logging
    def build(self, timetable):
        maps = [self.time_map(s, s+t) for s, t in timetable if self.at_date(s)]
        return self.delim.join([self.template.substitute(m) for m in maps])

    @Logger.logging
    def at_date(self, ts):
        return self.t00 <= ts and ts < self.t24

    @Logger.logging
    def time_map(self, s, e):
        start = datetime.datetime.fromtimestamp(s)
        end = datetime.datetime.fromtimestamp(e)
        return {'SHOUR': start.hour, 'SMIN': '{:02}'.format(start.minute),
                'EHOUR': end.hour, 'EMIN': '{:02}'.format(end.minute)}
