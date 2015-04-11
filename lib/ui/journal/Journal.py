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
from lib.common.exceptions import JournalManagerNoExistTaskOfMemoError
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
        date, attrs, memos = self.read()

        # ファイルシステムにコミットする
        commit_task_num = self.commit_task(date, attrs)

        # メモのタスクが存在するか確認する
        for memo in memos:
            if not Tasktory.istask(memo["PATH"]):
                raise JournalManagerNoExistTaskOfMemoError(memo["PATH"])

        # メモをコミットする
        now = datetime.datetime.now()
        for memo in memos:
            Tasktory.restore(memo["PATH"]).memo.put(now, memo["TEXT"])
            self.info("MEMO", memo["PATH"])

        return commit_task_num, len(memos)

    # タスクをコミットする
    # コミットしたタスクの数を返す
    @Logger.logging
    def commit_task(self, date, attrs):

        # コミットしたタスクの数
        commit_num = 0

        # タスクを作成する
        if not attrs:
            return 0
        leafs, inners = zip(*(self.tb.build(attr) for attr in attrs))
        # leafs, inners = zip(*map(self.tb.build, attrs))

        # 当日の午前零時から翌日の午前零時
        a = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        b = a + datetime.timedelta(1)
        a = int(a.timestamp())
        b = int(b.timestamp())

        def at_date(t):
            return a <= t[0] and t[0] < b

        # 内部ノードは存在しないもののみコミットする
        for task in sum(inners, []):
            if not Tasktory.istask(task.path):
                task.sync()
                commit_num += 1
                self.info("CREATE", str(task))

        # 葉ノードは変更があるもののみコミットする
        for task in leafs:
            # 存在しなければコミットする
            if not Tasktory.istask(task.path):
                task.sync()
                commit_num += 1
                self.info("CREATE", str(task))
                continue

            # 既存のタスクを復元する
            org = Tasktory.restore(task.path)

            # 変更が無ければ無視する
            if all([
                    org.deadline == task.deadline,
                    org.status == task.status,
                    set(filter(at_date, org.timetable)) == set(task.timetable),
                    org.comment == task.comment,
                    ]):
                continue

            # 当日分の作業時間を削除する
            org.timetable = [t for t in org.timetable if not at_date(t)]

            # マージしてコミットする
            org.merge(task).sync()
            commit_num += 1
            self.info("UPDATE", str(task))

        return commit_num
