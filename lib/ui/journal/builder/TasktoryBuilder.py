#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.common import convolute
from lib.core.Tasktory import Tasktory
from lib.log.Logger import Logger


class TasktoryBuilder(Logger):
    """ジャーナル解析結果からタスクトリインスタンスを作成する"""

    def __init__(self, config):
        self.root = config['Main']['ROOT']
        super().__init__()
        return

    @Logger.logging
    def build(self, attrs):
        names = attrs['PATH'].split('/')
        paths = convolute(lambda p, a: (a+'/'+p if a+p else p,)*2, names, '')
        tasks = [self.node(p, attrs) for p in paths]
        return tasks[-1], tasks[:-1]

    @Logger.logging
    def node(self, path, attrs):
        return self.leaf(attrs) if path == attrs['PATH']\
                else self.inner(path, attrs)

    @Logger.logging
    def inner(self, path, attrs):
        return Tasktory(self.root + path, attrs['DEADLINE'], Tasktory.OPEN, '')

    @Logger.logging
    def leaf(self, attrs):
        task = Tasktory(
                self.root + attrs['PATH'],
                attrs['DEADLINE'], attrs['STATUS'], attrs['COMMENT'])
        for start, sec in attrs['TIMETABLE']:
            task.punch(start, sec)
        return task
