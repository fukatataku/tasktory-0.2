# -*- coding: utf-8 -*-

import os
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
from lib.ui.journal.parser.JournalParser import JournalParser
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
        self.root = config['Main']['ROOT']
        self.journal = config['Main']['JOURNAL']
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
        return

    # JournalObject -> FileSystem
    def save(self):
        return

    # TextFile -> JournalObject
    def read(self):
        # ジャーナルが存在しなければNoneを返す
        if not os.path.isfile(self.journal):
            return None

        # ジャーナルテキストを読み出す
        with open(self.journal, "r", encoding="utf-8-sig") as f:
            text = f.read()

        # ジャーナルを解析する
        date, attrs_list, memo_list = self.jp.parse(text)

    # JournalObject -> TextFile
    def write(self):
        return


class Journal:

    def __init__(self):
        return
