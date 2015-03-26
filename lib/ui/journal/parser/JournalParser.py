#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from lib.core.Tasktory import Tasktory
from lib.common.Regexplate import Regexplate
from lib.ui.journal.parser.TaskChunkParser import TaskChunkParser
from lib.ui.journal.parser.MemoParser import MemoParser
from lib.common.common import convolute
from lib.common.exceptions import JournalParserDuplicateTaskError
from lib.common.exceptions import JournalParserOverlapTimeTableError


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
        date = datetime.date(
                int(attrs['YEAR']), int(attrs['MONTH']), int(attrs['DAY']))

        # 各タスクチャンクをパース
        tcp = TaskChunkParser(date, self.config)
        tasks = [
                self.ps(d, Tasktory.OPEN)
                for d in tcp.parse(attrs['OPENCHUNK'])]
        tasks += [
                self.ps(d, Tasktory.WAIT)
                for d in tcp.parse(attrs['WAITCHUNK'])]
        tasks += [
                self.ps(d, Tasktory.CLOSE)
                for d in tcp.parse(attrs['CLOSECHUNK'])]

        # タスクの重複チェック
        if self.duplicate_task(tasks):
            raise JournalParserDuplicateTaskError()

        # 作業時間の重複チェック
        if self.duplicate_timetable(tasks):
            raise JournalParserOverlapTimeTableError()

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
        tbl = sorted(
                sum([t['TIMETABLE'] for t in tasks], []),
                key=lambda t: t[0])
        return not all(convolute(
            lambda v, a: (sum(a) <= v[0], v), tbl, (0, 0)
            ))

    @staticmethod
    def ps(d, s):
        d['STATUS'] = s
        return d
