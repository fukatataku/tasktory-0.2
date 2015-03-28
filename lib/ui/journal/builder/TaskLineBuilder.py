#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.Regexplate import Regexplate
from lib.ui.journal.builder.DeadLineBuilder import DeadLineBuilder
from lib.ui.journal.builder.TimeTableBuilder import TimeTableBuilder
from lib.log.Logger import Logger


class TaskLineBuilder(Logger):
    """"""

    def __init__(self, date, config):
        self.root = config['Main']['ROOT']
        self.dlb = DeadLineBuilder(date, config)
        self.ttb = TimeTableBuilder(date, config)
        self.template = Regexplate(config['Journal']['TASKLINE'])
        super().__init__()

    @Logger.logging
    def build(self, task):
        return self.template.substitute(self.task_map(task))

    @Logger.logging
    def task_map(self, task):
        return {
                'PATH': self.short_path(task.path),
                'DEADLINE': self.dlb.build(task.deadline),
                'TIMETABLE': self.ttb.build(task.timetable),
                }

    @Logger.logging
    def short_path(self, path):
        if self.root not in path or path.index(self.root) != 0:
            return path
        else:
            return path.replace(self.root, '')
