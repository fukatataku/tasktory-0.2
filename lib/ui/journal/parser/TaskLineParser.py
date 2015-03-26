#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.Regexplate import Regexplate
from lib.ui.journal.parser.TimeTableParser import TimeTableParser
from lib.ui.journal.parser.DeadLineParser import DeadLineParser


class TaskLineParser:
    """タスクライン解析器"""

    def __init__(self, date, config):
        self.dlp = DeadLineParser(date, config)
        self.ttp = TimeTableParser(date, config)
        self.template = Regexplate(config['Journal']['TASKLINE'])

    def parse(self, string):
        attrs = self.template.parse(string)
        return {'PATH': attrs['PATH'],
                'DEADLINE': self.dlp.parse(attrs['DEADLINE']),
                'TIMETABLE': self.ttp.parse(attrs['TIMETABLE'])}

    def match(self, string):
        return self.template.match(string)
