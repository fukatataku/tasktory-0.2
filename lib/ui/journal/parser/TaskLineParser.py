#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.Regexplate import Regexplate
from lib.ui.journal.parser.TimeTableParser import TimeTableParser
from lib.ui.journal.parser.DeadLineParser import DeadLineParser
from lib.log.Logger import Logger


class TaskLineParser(Logger):
    """タスクライン解析器"""

    def __init__(self, date, config):
        self.dlp = DeadLineParser(date, config)
        self.ttp = TimeTableParser(date, config)
        self.template = Regexplate(config['Journal']['TASKLINE'])
        super().__init__()
        return

    @Logger.logging
    def parse(self, string):
        attrs = self.template.parse(string)
        return {'PATH': attrs['PATH'],
                'DEADLINE': self.dlp.parse(attrs['DEADLINE']),
                'TIMETABLE': self.ttp.parse(attrs['TIMETABLE'])}

    @Logger.logging
    def match(self, string):
        return self.template.match(string)
