#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.Regexplate import Regexplate
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.TaskChunkBuilder import TaskChunkBuilder
from lib.log.Logger import Logger


class JournalBuilder(Logger):

    def __init__(self, tmpl, config):
        self.template = Regexplate(tmpl)
        self.config = config
        super().__init__()

    @Logger.logging
    def build(self, date, tasks, memo):
        self.tcb = TaskChunkBuilder(date, self.config)
        return self.template.substitute({
            'YEAR': date.year, 'MONTH': date.month, 'DAY': date.day,
            'OPENCHUNK': self.tcb.build(
                [t for t in tasks if t.status == Tasktory.OPEN]),
            'WAITCHUNK': self.tcb.build(
                [t for t in tasks if t.status == Tasktory.WAIT]),
            'CLOSECHUNK': self.tcb.build(
                [t for t in tasks if t.status == Tasktory.CLOSE]),
            'MEMO': memo,
            })
