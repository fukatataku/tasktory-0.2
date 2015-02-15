# -*- coding: utf-8 -*-

import datetime, re
from lib.common.Regexplate import Regexplate
from lib.ui.journal.parser.TaskChunkParser import TaskChunkParser
from lib.ui.journal.parser.MemoParser import MemoParser

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
        tasks = [ps(d,Tasktory.OPEN) for d in tcp.parse(attrs['OPENCHUNK'])]
        tasks += [ps(d,Tasktory.WAIT) for d in tcp.parse(attrs['WAITCHUNK'])]
        tasks += [ps(d,Tasktory.CLOSE) for d in tcp.parse(attrs['CLOSECHUNK'])]

        # メモを取得
        memo = self.mp.parse(attrs['MEMO'])

        return date, tasks, memo

    @staticmethod
    def ps(d, s):
        d['STATUS'] = s
        return d
