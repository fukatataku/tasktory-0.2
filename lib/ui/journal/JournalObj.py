# -*- coding: utf-8 -*-

import os
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
from lib.ui.journal.parser.JournalParser import JournalParser
from lib.ui.journal.builder.TasktoryBuilder import TasktoryBuilder
from lib.utility.filter.TasktoryFilter import TasktoryFilter
from lib.common.common import unique
from lib.common.common import JRNL_TMPL_FILE


class JournalManager:

    def __init__(self, config, filt_config):
        with open(JRNL_TMPL_FILE) as f:
            tmpl = f.read()
        self.jb = JournalBuilder(tmpl, config)
        self.jp = JournalParser(tmpl, config)
        self.jf = TasktoryFilter.get_filter(filt_config['JournalFilter'])
        self.tb = TasktoryBuilder(config)
        self.root = config['Main']['ROOT']
        self.journal_path = config['Main']['JOURNAL']
        return

    # FileSystem -> JournalObject
    def load(self, date):
        # ファイルシステムからタスクを復元する
        root_task = Tasktory.restore(self.root)
        if root_task is None:
            tasks = []
        else:
            tasks = self.jf.select(root_task)

        # tasksのuniqueを取る
        tasks = unique(tasks, lambda t: t.path)

        # ジャーナルオブジェクトを作成する
        return Journal(tasks)

    # JournalObject -> FileSystem
    def save(self, journal):
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

        # メモ

        return Journal(tasks)

    # JournalObject -> TextFile
    def write(self, journal):
        return


class Journal:

    def __init__(self, tasks, memos=[]):
        self.tasks = tasks
        self.memos = memos
        return

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
