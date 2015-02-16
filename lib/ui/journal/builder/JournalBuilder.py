#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

import datetime
from lib.common.Regexplate import Regexplate
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.TaskChunkBuilder import TaskChunkBuilder

class JournalBuilder:

    def __init__(self, tmpl, config):
        self.template = Regexplate(tmpl)
        self.config = config

    def build(self, date, tasks):
        self.tcb = TaskChunkBuilder(date, self.config)
        return self.template.substitute({
            'YEAR': date.year, 'MONTH': date.month, 'DAY': date.day,
            'OPENCHUNK': self.tcb.build(
                [t for t in tasks if t.status == Tasktory.OPEN]),
            'WAITCHUNK': self.tcb.build(
                [t for t in tasks if t.status == Tasktory.WAIT]),
            'CLOSECHUNK': self.tcb.build(
                [t for t in tasks if t.status == Tasktory.CLOSE]),
            'MEMO': '',
            })

if __name__ == '__main__':
    import configparser
    from lib.core.Tasktory import Tasktory
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    t = []
    t.append(Tasktory('/path/to/task0', today.toordinal(), Tasktory.OPEN,
        'あいうえお\nかきくけこ'))
    t.append(Tasktory('/path/to/task1', today.toordinal() + 1, Tasktory.OPEN, ''))
    t.append(Tasktory('/path/to/task2', today.toordinal(), Tasktory.WAIT, ''))
    t.append(Tasktory('/path/to/task3', today.toordinal(), Tasktory.CLOSE, ''))

    tmpl_path = path('../../../../res/template/journal.tmpl')
    with open(tmpl_path) as f:
        tmpl = f.read()

    jb = JournalBuilder(tmpl, config)
    print(jb.build(today, t))
