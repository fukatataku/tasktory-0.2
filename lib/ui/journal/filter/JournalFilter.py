# -*- coding: utf-8 -*-

from lib.core.Task import Task

class JournalFilter:
    """ジャーナル書き出し用タスクフィルタ"""

    def ok(self, task):
        if task.status == Task.OPEN:
            return False if task.deadline == float('inf') else True
        elif task.status == Task.WAIT:
            return True
        elif task.status == Task.CLOSE:
            return False
        else:
            return False
