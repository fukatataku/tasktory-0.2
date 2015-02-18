#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

import datetime, re
from lib.core.Tasktory import Tasktory
from lib.common.Regexplate import Regexplate
from lib.ui.journal.parser.TaskChunkParser import TaskChunkParser
from lib.ui.journal.parser.MemoParser import MemoParser

from lib.common.common import convolute

class JournalParser:
    """ジャーナル解析器"""

    def __init__(self, tmpl, config):
        self.template = Regexplate(tmpl)
        self.config = config
        self.mp = MemoParser(config)

    def parse(self, text):
        # ジャーナルをパース
        attrs = self.template.parse(text)

        # 日付を取得
        date = datetime.date(int(attrs['YEAR']),
                int(attrs['MONTH']), int(attrs['DAY']))

        # 各タスクチャンクをパース
        tcp = TaskChunkParser(date, self.config)
        tasks = [self.ps(d,Tasktory.OPEN)
                for d in tcp.parse(attrs['OPENCHUNK'])]
        tasks += [self.ps(d,Tasktory.WAIT)
                for d in tcp.parse(attrs['WAITCHUNK'])]
        tasks += [self.ps(d,Tasktory.CLOSE)
                for d in tcp.parse(attrs['CLOSECHUNK'])]

        # タスクの重複チェック
        if self.duplicate_task(tasks): raise RuntimeError()

        # 作業時間の重複チェック
        if self.duplicate_timetable(tasks): raise RuntimeError()

        # メモを取得
        memo = self.mp.parse(attrs['MEMO'])

        return date, tasks, memo

    @staticmethod
    def duplicate_task(tasks):
        """同じタスクが複数存在する場合Trueを返す"""
        return len(tasks) != len(set([t['PATH'] for t in tasks]))

    @staticmethod
    def duplicate_timetable(tasks):
        """作業時間に重複があればTrueを返す"""
        tbl = sorted(sum([t['TIMETABLE'] for t in tasks], []), key=lambda t:t[0])
        return not all(convolute(lambda v,a:(sum(a)<=v[0], v), tbl, (0, 0)))

    @staticmethod
    def ps(d, s):
        d['STATUS'] = s
        return d

if __name__ == '__main__':
    times = [[(0,10), (10,10)], [(20, 10), (30, 20), (70, 100)], [(180, 20)]]
    table = sorted(sum(times, []), key=lambda t:t[0])
    dup = convolute(lambda v,a:(sum(a)<=v[0], v), table, (0, 0))
    print(not all(dup))
