#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.common.Regexplate import Regexplate
from lib.ui.journal.parser.TimeTableParser import TimeTableParser
from lib.ui.journal.parser.DeadLineParser import DeadLineParser

class TaskLineParser:
    """タスクライン解析器"""

    def __init__(self, date, config):
        self.root = config['Main']['ROOT']
        self.dlp = DeadLineParser(date, config)
        self.ttp= TimeTableParser(date, config)
        self.template = Regexplate(config['Journal']['TASKLINE'])

    def parse(self, string):
        attrs = self.template.parse(string)
        return {'PATH': self.root + attrs['PATH'],
                'DEADLINE': self.dlp.parse(attrs['DEADLINE']),
                'TIMETABLE': self.ttp.parse(attrs['TIMETABLE'])}

    def match(self, string):
        return self.template.match(string)

if __name__ == '__main__':
    # コンフィグ
    import configparser
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    tlp = TaskLineParser(today, config)
    print(tlp.parse('/path/to/task @0 []'))
    print(tlp.parse('/path @1 [9:00-12:00]'))
    print(tlp.parse(' @@ [9:00-12:00,13:00-15:00]'))

    print(tlp.match('/path/to/task @0 []'))
