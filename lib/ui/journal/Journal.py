#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../'))

import os
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
from lib.ui.journal.builder.TasktoryBuilder import TasktoryBuilder
from lib.ui.journal.parser.JournalParser import JournalParser
from lib.ui.journal.filter.JournalFilter import JournalFilter

from lib.common.common import JRNL_TMPL_FILE

class Journal:
    """"""

    def __init__(self, config):
        with open(JRNL_TMPL_FILE) as f:
            tmpl = f.read()
        self.jb = JournalBuilder(tmpl, config)
        self.jp = JournalParser(tmpl, config)
        self.jf = JournalFilter()
        self.tb = TasktoryBuilder(config)
        self.root = config['Main']['ROOT']
        self.journal = config['Main']['JOURNAL']

    def checkout(self, date):
        # ファイルシステムからタスクを復元する
        root_task = Tasktory.restore(self.root)
        tasks = [] if root_task is None\
                else [t for t in root_task if self.jf.ok(t)]

        # ジャーナルディレクトリを作成する
        os.makedirs(os.path.dirname(self.journal), exist_ok=True)

        # ジャーナルを書き出す
        with open(self.journal, 'w', encoding='utf-8') as f:
            f.write(self.jb.build(date, tasks))

    def commit(self):
        # ジャーナルを読み出す
        with open(self.journal, 'r', encoding='utf-8-sig') as f:
            self.text = f.read()

        # ジャーナルを解析する
        date, attrs_list, memo = self.jp.parse(self.text)

        # ファイルシステムにコミットする
        for attrs in attrs_list:
            leaf, inners = self.tb.build(attrs)

            # 葉ノードタスクトリをコミットする
            org = Tasktory.restore(leaf.path)
            if org is None:
                leaf.sync()
            else:
                org.merge(leaf).sync()

            # 内部ノードタスクトリをコミットする
            for t in inners:
                org = Tasktory.restore(t.path)
                if org is None: t.sync()

if __name__ == '__main__':
    # コンフィグ
    import configparser
    from lib.common.common import MAIN_CONF_FILE
    today = datetime.date.today()
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    journal = Journal(config)
    journal.checkout(today)
    #journal.commit()
