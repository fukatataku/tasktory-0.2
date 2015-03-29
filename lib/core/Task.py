# -*- coding: utf-8 -*-

from datetime import datetime, date
from lib.log.Logger import Logger


class Task(Logger):

    OPEN = 0
    WAIT = 1
    CLOSE = 2

    def __init__(self, deadline, status, comment):
        # 期日
        self.deadline = deadline
        # ステータス
        self.status = status
        # タイムテーブル（開始エポック秒と作業時間（秒）のタプルのリスト）
        self.timetable = []
        # コメント
        self.comment = comment

        super().__init__()

    def __bool__(self):
        return True

    @Logger.logging
    def total(self):
        """合計作業時間（秒）を返す"""
        return sum(t for _, t in self.timetable)

    @Logger.logging
    def timestamp(self):
        """タイムテーブル中の最大の終了エポック秒を返す"""
        if self.timetable:
            return sum(sorted(self.timetable, key=lambda t: t[0])[-1])
        else:
            return 0

    @Logger.logging
    def at(self, _from, to=None):
        """指定した期間に作業時間が計上されているかどうかを返す"""
        if to is None:
            to = _from
        if isinstance(_from, date):
            _from = int(datetime.fromordinal(_from.toordinal()).timestamp())
        if isinstance(to, date):
            to = int(datetime.fromordinal(to.toordinal() + 1).timestamp())

        for s, t in self.timetable:
            if _from < s+t and s <= to:
                return True
        return False

    @Logger.logging
    def merge(self, other):
        """タスクの差分をマージする"""
        if other.deadline is not None:
            self.deadline = other.deadline
        if other.status is not None:
            self.status = other.status
        self.timetable += other.timetable
        self.comment = other.comment
        return

    @Logger.logging
    def punch(self, start, sec):
        """作業時間（開始エポック秒、作業秒数）を追加する"""
        self.timetable.append((start, sec))
        return
