#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
from lib.ui.journal.builder.TasktoryBuilder import TasktoryBuilder
from lib.ui.journal.parser.JournalParser import JournalParser
from lib.utility.filter.TasktoryFilter import TasktoryFilter
from lib.common.common import unique
from lib.common.common import JRNL_TMPL_FILE
from lib.log.Logger import Logger


class Journal(Logger):
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
        super().__init__()
        return

    @Logger.logging
    def checkout(self, date):
        # TODO チェックアウト時にメモを残す？
        # 既存のジャーナルからメモを読み出す
        # _, _, memo_list = self.read()

        # ファイルシステムからタスクを復元する
        root_task = Tasktory.restore(self.root)
        if root_task is None:
            tasks = []
        else:
            tasks = self.jf.select(root_task)

        # tasksのuniqを取る
        tasks = unique(tasks, lambda t: t.path)

        # ジャーナルディレクトリを作成する
        os.makedirs(os.path.dirname(self.journal), exist_ok=True)

        # ジャーナルを書き出す
        with open(self.journal, 'w', encoding='utf-8') as f:
            f.write(self.jb.build(date, tasks))

    @Logger.logging
    def read(self):
        # ジャーナルが存在しなければNoneを返す?
        if not os.path.isfile(self.journal):
            return datetime.datetime.now(), [], []

        # ジャーナルを読み出す
        with open(self.journal, 'r', encoding='utf-8-sig') as f:
            text = f.read()

        # ジャーナルを解析する
        return self.jp.parse(text)

    @Logger.logging
    def commit(self):
        # ジャーナルを解析する
        date, attrs_list, memo_list = self.read()

        # ファイルシステムにコミットする
        for attrs in attrs_list:
            self.__commit(date, attrs)

        # メモをコミットする
        for memo in memo_list:
            Tasktory.restore(memo['PATH']).memo.put(
                    datetime.datetime.now(), memo['TEXT'])

    @Logger.logging
    def __commit(self, date, attrs):
        leaf, inners = self.tb.build(attrs)

        # 葉ノードタスクトリをコミットする
        org = Tasktory.restore(leaf.path)
        if org is None:
            leaf.sync()
        else:
            # マージする前に当日の作業時間を削除する
            org.timetable = [t for t in org.timetable if not t.at(date)]
            org.merge(leaf).sync()

        # 内部ノードタスクトリをコミットする
        for t in inners:
            org = Tasktory.restore(t.path)
            if org is None:
                t.sync()
