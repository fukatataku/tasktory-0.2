#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.ui.journal.builder.TaskLineBuilder import TaskLineBuilder
from lib.ui.journal.builder.CommentBuilder import CommentBuilder

class TaskChunkBuilder:

    def __init__(self, date, config):
        self.tlb = TaskLineBuilder(date, config)
        self.cb = CommentBuilder()

    def build(self, tasks):
        return ''.join([self.build_task(task) for task in tasks])

    def build_task(self, task):
        return self.tlb.build(task) + '\n' +\
                (self.build_comment(task.comment) if task.comment else '')

    def build_comment(self, comment):
        return ''.join([self.cb.build(c) + '\n' for c in comment.split('\n')])

if __name__ == '__main__':
    import configparser
    from lib.core.Tasktory import Tasktory
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    t0 = Tasktory('C:/home/fukata/work/path/to/task0', today.toordinal(), 0, '')
    t1 = Tasktory('C:/home/fukata/work/path/to/task1', today.toordinal(), 0, 'hoge\nfuga')
    t2 = Tasktory('C:/home/fukata/work/path/to/task2', today.toordinal(), 0, 'hoge\nfuga')

    tcb = TaskChunkBuilder(today, config)
    print(tcb.build([t0, t1, t2]))
