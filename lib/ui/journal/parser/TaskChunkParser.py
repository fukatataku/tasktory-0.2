#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.common.common import convolute
from lib.core.Tasktory import Tasktory
from lib.ui.journal.parser.TaskLineParser import TaskLineParser
#from lib.ui.journal.parser.PathAliasParser import PathAliasParser
from lib.ui.journal.parser.CommentParser import CommentParser

class TaskChunkParser:
    """タスクチャンク解析機"""

    def __init__(self, date, config):
        #self.root = config['Main']['ROOT']
        #self.pap = PathAliasParser(config)
        self.tlp = TaskLineParser(date, config)
        self.cp = CommentParser()

    def parse(self, chunk):
        items = [item for item in chunk.split("\n") if item.strip() != ""]

        # タスクラインをパースする（ついでにパスエイリアスを解決する）
        #parse_taskline = lambda v,a: self.parse_taskline(v, a)
        #items = convolute(parse_taskline, items, "")

        # タスクラインをパースする
        parse = lambda v: self.tlp.parse(v) if self.tlp.match(v) else v
        items = [parse(item) for item in items]

        # 用済みになったパスエイリアスを取り除く
        #items = [v for v in items
        #        if isinstance(v, dict) or not self.pap.match(v)]

        # コメントを解決する
        solve_comment = lambda v,a: self.solve_comment(v, a)
        items = reversed(convolute(solve_comment, reversed(items), ""))

        # 用済みになったコメントを取り除く
        items = [v for v in items if not self.cp.match(v)]

        return items

    #def parse_taskline(self, v, a):
    #    if self.pap.match(v):
    #        return v, self.pap.parse(v)['PATH']
    #    elif self.tlp.match(v):
    #        d = self.tlp.parse(v)
    #        d['PATH'] = self.root + a + d['PATH']
    #        return d, a
    #    else:
    #        return v, a

    def solve_comment(self, v, a):
        if self.cp.match(v):
            return v, self.cp.parse(v)['COMMENT'] + ("\n" + a if a else a)
        elif isinstance(v, dict):
            v['COMMENT'] = a
            return v, ""
        else:
            return v, a

if __name__ == '__main__':
    # コンフィグ
    import configparser
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    tcp = TaskChunkParser(today, config)

    chunk = """
/A/make @0 []
/A/review @10 [9:00-10:00, 17:45-18:00]
 # hogehoge
 # fugafuga
/B/make @@ [10:00-12:00]
/B/review @20 [13:00-15:00,15:00-17:45]
"""

    for t in tcp.parse(chunk):
        print(t)
