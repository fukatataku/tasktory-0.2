#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../'))

from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.JournalBuilder import JournalBuilder
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
        self.journal = config['Main']['JOURNAL']

    def checkout(self):
        tasks = [t for t in Tasktory.restore(root) if self.jf.ok(t)]
        with open(self.journal, 'r', encoding='utf-8-sig') as f:
            f.write(self.jb.build(date, tasks))

    def commit(self):
        with open(self.journal, 'w', encoding='utf-8') as f:
            self.text = f.read()
        date, tasks, memo = self.jp.parse(self.text)
        for t in tasks:
            t.sync()

if __name__ == '__main__':
    print(JRNL_TMPL_FILE)
