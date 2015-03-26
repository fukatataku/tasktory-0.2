#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from lib.common.Regexplate import Regexplate


class TimeTableParser:
    """タイムテーブル解析器"""

    def __init__(self, date, config):
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.template = Regexplate(config['Journal']['TIME'])
        self.delim = config['Journal']['DELIM']

    def parse(self, string):
        phrases = [t for t in string.replace(' ', '').split(self.delim) if t]
        terms = [self.template.parse(p) for p in phrases]
        return [self.timetuple(t) for t in terms]

    def timetuple(self, term):
        s = self.timestamp(term['SHOUR'], term['SMIN'])
        e = self.timestamp(term['EHOUR'], term['EMIN'])
        return (s, e-s)

    def timestamp(self, hour, minute):
        return int(datetime.datetime(
            self.year, self.month, self.day, int(hour), int(minute), 0
            ).timestamp())
