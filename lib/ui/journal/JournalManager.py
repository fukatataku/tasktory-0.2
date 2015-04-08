# -*- coding: utf-8 -*-

import os
import datetime
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
from lib.ui.journal.parser.JournalParser import JournalParser
from lib.ui.journal.builder.TasktoryBuilder import TasktoryBuilder
from lib.utility.filter.TasktoryFilter import TasktoryFilter
from lib.common.common import unique
from lib.common.common import JRNL_TMPL_FILE
from lib.common.exceptions import JournalManagerNoExistTaskOfMemoError
from lib.log.Logger import Logger


class JournalManager(Logger):

    def __init__(self, config, filt_config):
        with open(JRNL_TMPL_FILE) as f:
            tmpl = f.read()
        self.jb = JournalBuilder(tmpl, config)
        self.jp = JournalParser(tmpl, config)
        self.jf = TasktoryFilter.get_filter(filt_config['JournalFilter'])
        self.tb = TasktoryBuilder(config)
        self.root = config['Main']['ROOT']
        self.journal_path = config['Main']['JOURNAL']
        super().__init__()
        return

    # FileSystem -> JournalObject
    def load(self, date):
        # ファイルシステムからタスクを復元する
        root_task = Tasktory.restore(self.root)
        tasks = [] if root_task is None else self.jf.select(root_task)

        # tasksのuniqueを取る
        tasks = unique(tasks, lambda t: t.path)

        # ジャーナルオブジェクトを作成する
        return Journal(date, tasks)

    # JournalObject -> FileSystem
    def save(self, journal):
        # タスクを保存する
        for task in journal.tasks:
            if Tasktory.istask(task.path):
                # TODO: 変更が無ければ無視する

                org = Tasktory.restore(task.path)
                org.timetable =\
                    [t for t in org.timetable if not t.at(journal.date)]
                org.merge(task).sync()
            else:
                task.sync()

        # メモを保存する
        for memo in journal.memos:
            task = Tasktory.restore(memo["PATH"])
            if task is None:
                raise JournalManagerNoExistTaskOfMemoError()
            task.memo.put(datetime.datetime.now(), memo["TEXT"])
        return

    # TextFile -> JournalObject
    def read(self):
        # ジャーナルが存在しなければNoneを返す
        if not os.path.isfile(self.journal_path):
            return None

        # ジャーナルテキストを読み出す
        with open(self.journal_path, "r", encoding="utf-8-sig") as f:
            text = f.read()

        # ジャーナルを解析する
        date, attrs_list, memo_list = self.jp.parse(text)

        # タスクリストを作成する
        tasks = []
        for attrs in attrs_list:
            leaf, inners = self.tb.build(attrs)
            tasks.append(leaf)
            tasks += [t for t in inners if not Tasktory.istask(t)]

        return Journal(date, tasks, memo_list)

    # JournalObject -> TextFile
    def write(self, journal):
        # ジャーナルディレクトリを作成する
        os.makedirs(os.path.dirname(self.journal_path), exist_ok=True)

        # 既存のジャーナルからメモ部分を取り出す

        # ジャーナルを書き出す
        with open(self.journal_path, "w", encoding="utf-8") as f:
            f.write(self.jb.build(journal.date, journal.tasks))
        return


class Journal(Logger):

    def __init__(self, date, tasks, memos=[]):
        self.date = date
        self.tasks = tasks
        self.memos = memos
        super().__init__()
        return

    def __eq__(self, other):
        if not type(self) == type(other):
            raise TypeError("other must be Journal instance")
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
