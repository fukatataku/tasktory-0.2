#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from lib.common.Regexplate import Regexplate


class DeadLineParser:
    """期日解析器"""

    def __init__(self, date, config):
        self.today = date
        self.num_reg = re.compile('^-?\d+$')
        self.infstr = config['Journal']['INFSTR']
        self.template = Regexplate(config['Journal']['DATE'])

    def parse(self, string):
        # @
        if string == '':
            return None

        # @@
        if string == self.infstr:
            return float('inf')

        # @d
        m = self.num_reg.match(string)
        if m:
            return self.today.toordinal() + int(m.group())

        date = self.template.parse(string)
        year = date['YEAR']
        month = int(date['MONTH'])
        day = int(date['DAY'])

        # @mm/dd
        if year is None:
            tmp_date = datetime.date(self.today.year, month, day)
            year = self.today.year + (0 if tmp_date >= self.today else 1)

        # @yy/mm/dd
        elif len(year) == 2:
            year = int(year) + self.today.year // 100 * 100
            tmp_date = datetime.date(year, month, day)
            year += 0 if tmp_date >= self.today else 100

        # YYYY/mm/dd
        else:
            year = int(year)

        return datetime.date(year, month, day).toordinal()
