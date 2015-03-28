#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.ui.journal.builder.TaskLineBuilder import TaskLineBuilder
from lib.ui.journal.builder.CommentBuilder import CommentBuilder
from lib.log.Logger import Logger


class TaskChunkBuilder(Logger):

    def __init__(self, date, config):
        self.tlb = TaskLineBuilder(date, config)
        self.cb = CommentBuilder()
        super().__init__()

    @Logger.logging
    def build(self, tasks):
        return ''.join([self.build_task(task) for task in tasks])

    @Logger.logging
    def build_task(self, task):
        return self.tlb.build(task) + '\n' +\
                (self.build_comment(task.comment) if task.comment else '')

    @Logger.logging
    def build_comment(self, comment):
        return ''.join([self.cb.build(c) + '\n' for c in comment.split('\n')])
