#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

import datetime, re
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
        if string == '': return None

        # @@
        if string == self.infstr: return float('inf')

        # @d
        m = self.num_reg.match(string)
        if m: return self.today.toordinal() + int(m.group())

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
            year = int(year) + today.year // 100 * 100
            tmp_date = datetime.date(year, month, day)
            year += 0 if tmp_date >= self.today else 100

        # YYYY/mm/dd
        else:
            year = int(year)

        return datetime.date(year, month, day).toordinal()

if __name__ == '__main__':
    # コンフィグ
    import configparser
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    dlp = DeadLineParser(today, config)
    print(dlp.parse(''))
    print(dlp.parse('0'))
    print(dlp.parse('@'))
    print(dlp.parse('12/24'))
    print(dlp.parse('12/23'))
    print(dlp.parse('14/12/24'))
    print(dlp.parse('2014/12/24'))
