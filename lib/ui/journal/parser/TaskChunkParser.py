#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.common import convolute
from lib.ui.journal.parser.TaskLineParser import TaskLineParser
from lib.ui.journal.parser.CommentParser import CommentParser
from lib.log.Logger import Logger


class TaskChunkParser(Logger):
    """タスクチャンク解析機"""

    def __init__(self, date, config):
        self.tlp = TaskLineParser(date, config)
        self.cp = CommentParser()
        super().__init__()
        return

    @Logger.logging
    def parse(self, chunk):
        items = [item for item in chunk.split("\n") if item.strip() != ""]

        # タスクラインをパースする
        items = [self.__parse(item) for item in items]

        # コメントを解決する
        items = reversed(convolute(self.solve_comment, reversed(items), ""))

        # 用済みになったコメントを取り除く
        items = [v for v in items if not self.cp.match(v)]

        return items

    @Logger.logging
    def __parse(self, item):
        return self.tlp.parse(item) if self.tlp.match(item) else item

    @Logger.logging
    def solve_comment(self, v, a):
        if self.cp.match(v):
            return v, self.cp.parse(v)['COMMENT'] + ("\n" + a if a else a)
        elif isinstance(v, dict):
            v['COMMENT'] = a
            return v, ""
        else:
            return v, a
