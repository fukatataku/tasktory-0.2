#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.ui.journal.builder.TaskLineBuilder import TaskLineBuilder
from lib.ui.journal.builder.CommentBuilder import CommentBuilder


class TaskChunkBuilder:

    def __init__(self, date, config):
        self.tlb = TaskLineBuilder(date, config)
        self.cb = CommentBuilder()

    def build(self, tasks):
        return ''.join([self.build_task(task) for task in tasks])

    def build_task(self, task):
        return self.tlb.build(task) + '\n' +\
                (self.build_comment(task.comment) if task.comment else '')

    def build_comment(self, comment):
        return ''.join([self.cb.build(c) + '\n' for c in comment.split('\n')])
