#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.common.Regexplate import Regexplate
from lib.ui.journal.builder.DeadLineBuilder import DeadLineBuilder
from lib.ui.journal.builder.TimeTableBuilder import TimeTableBuilder

class TaskLineBuilder:
    """"""

    def __init__(self, date, config):
        self.root = config['Main']['ROOT']
        self.dlb = DeadLineBuilder(date, config)
        self.ttb = TimeTableBuilder(date, config)
        self.template = Regexplate(config['Journal']['TASKLINE'])

    def build(self, task):
        return self.template.substitute(self.task_map(task))

    def task_map(self, task):
        return {
                'PATH': self.short_path(task.path),
                'DEADLINE': self.dlb.build(task.deadline),
                'TIMETABLE': self.ttb.build(task.timetable),
                }

    def short_path(self, path):
        if self.root not in path or path.index(self.root) != 0:
            return path
        else:
            return path.replace(self.root, '')

if __name__ == '__main__':
    import configparser
    from lib.core.Tasktory import Tasktory
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    tlb = TaskLineBuilder(today, config)

    t = Tasktory('C:/home/fukata/work/path/to/task', today.toordinal(), 0, '')
    print(tlb.build(t))
