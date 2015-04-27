# -*- coding: utf-8 -*-

from lib.core.Task import Task
from lib.log.Logger import Logger


class JournalTester(Logger):

    def __init__(self, date=None):
        self.date = date
        self.tests_list = [
                [
                    lambda t: t.status == Task.OPEN,
                    lambda t: t.deadline != float("inf"),
                    ],
                [
                    lambda t: t.status == Task.WAIT,
                    ],
                [
                    lambda t: t.status == Task.CLOSE,
                    lambda t: t.at(self.date),
                    ],
                ]
        return

    @Logger.logging
    def test(self, task):
        for tests in self.tests_list:
            if all([t(task) for t in tests]):
                return True
        return False
