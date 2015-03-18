#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
from lib.ui.journal.builder.TasktoryBuilder import TasktoryBuilder
from lib.ui.journal.parser.JournalParser import JournalParser
from lib.filter.TasktoryFilter import TasktoryFilter

from lib.common.common import JRNL_TMPL_FILE


class Journal:
    """"""

    def __init__(self, config, filt_config):
        with open(JRNL_TMPL_FILE) as f:
            tmpl = f.read()
        self.jb = JournalBuilder(tmpl, config)
        self.jp = JournalParser(tmpl, config)
        self.jf = TasktoryFilter.get_filter(filt_config['JournalFilter'])
        self.tb = TasktoryBuilder(config)
        self.root = config['Main']['ROOT']
        self.journal = config['Main']['JOURNAL']

    def checkout(self, date):
        # TODO チェックアウト時にメモを残す？
        # 既存のジャーナルからメモを読み出す
        # _, _, memo_list = self.read_journal()

        # ファイルシステムからタスクを復元する
        root_task = Tasktory.restore(self.root)
        if root_task is None:
            tasks = []
        else:
            tasks = self.jf.select(root_task)

        # ジャーナルディレクトリを作成する
        os.makedirs(os.path.dirname(self.journal), exist_ok=True)

        # ジャーナルを書き出す
        with open(self.journal, 'w', encoding='utf-8') as f:
            f.write(self.jb.build(date, tasks))

    def read_journal(self):
        # ジャーナルが存在しなければNoneを返す?
        if not os.path.isfile(self.journal):
            return datetime.datetime.now(), [], []

        # ジャーナルを読み出す
        with open(self.journal, 'r', encoding='utf-8-sig') as f:
            text = f.read()

        # ジャーナルを解析する
        return self.jp.parse(text)

    def commit(self):
        # ジャーナルを解析する
        date, attrs_list, memo_list = self.read_journal()

        # ファイルシステムにコミットする
        for attrs in attrs_list:
            self.commit_one(date, attrs)

        # メモをコミットする
        for memo in memo_list:
            Tasktory.restore(memo['PATH']).memo.put(
                    datetime.datetime.now(), memo['TEXT'])

    def commit_one(self, date, attrs):
        leaf, inners = self.tb.build(attrs)

        # 葉ノードタスクトリをコミットする
        org = Tasktory.restore(leaf.path)
        if org is None:
            leaf.sync()
        else:
            # マージする前に当日の作業時間を削除する
            org.timetable =\
                [t for t in org.timetable if not self.at(date, t[0])]
            org.merge(leaf).sync()

        # 内部ノードタスクトリをコミットする
        for t in inners:
            org = Tasktory.restore(t.path)
            if org is None:
                t.sync()

    @staticmethod
    def at(date, ts):
        a = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        b = a + datetime.timedelta(1)
        return int(a.timestamp()) <= ts and ts < int(b.timestamp())
