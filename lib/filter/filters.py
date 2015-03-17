#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from lib.core.Tasktory import Tasktory


# =============================================================================
# メタクラス／ベースクラス
# =============================================================================

# フィルタークラスを文字列で指定して参照できるようにするためのメタクラス
class FilterFactory(type):

    __CLASSES = {}

    def __new__(cls, name, bases, namespace):
        new_class = type.__new__(cls, name, bases, namespace)
        cls.__CLASSES[name] = new_class
        return new_class

    @classmethod
    def get_filter(cls, name):
        return cls.__CLASSES[name]


# フィルタのベースクラス
class TasktoryFilter(metaclass=FilterFactory):
    def select(self, tasks):
        return [t for t in tasks if self.test(t)]

    def reject(self, tasks):
        return [t for t in tasks if not self.test(t)]


# =============================================================================
# 期日フィルタ
# =============================================================================

# 期日が特定の値
class DeadLineFilter(TasktoryFilter):
    def __init__(self, deadline):
        self.test = lambda t: t.deadline == deadline
        return


# 期日が特定の値でない
class DeadLineIsNotFilter(TasktoryFilter):
    def __init__(self, deadline):
        self.test = lambda t: t.deadline != deadline
        return


# 期日が無期限でない
class DeadLineIsNotInfiniteFilter(DeadLineIsNotFilter):
    def __init__(self):
        return super().__init__(float('inf'))


# =============================================================================
# ステータスフィルタ
# =============================================================================

# 特定のステータスである
class StatusFilter(TasktoryFilter):
    def __init__(self, status):
        self.test = lambda t: t.status == status
        return


# ステータスがOPENである
class StatusIsOpenFilter(StatusFilter):
    def __init__(self):
        return super().__init__(Tasktory.OPEN)


# ステータスがWAITである
class StatusIsWaitFilter(StatusFilter):
    def __init__(self):
        return super().__init__(Tasktory.WAIT)


# ステータスがCLOSEである
class StatusIsCloseFilter(StatusFilter):
    def __init__(self):
        return super().__init__(Tasktory.CLOSE)


# 特定のステータスでない
class StatusIsNotFilter(TasktoryFilter):
    def __init__(self, status):
        self.test = lambda t: t.status != status
        return


# ステータスがOPENでない
class StatusIsNotOpenFilter(StatusIsNotFilter):
    def __init__(self):
        return super().__init__(Tasktory.OPEN)


# ステータスがWAITでない
class StatusIsNotWaitFilter(StatusIsNotFilter):
    def __init__(self):
        return super().__init__(Tasktory.WAIT)


# ステータスがCLOSEでない
class StatusIsNotCloseFilter(StatusIsNotFilter):
    def __init__(self):
        return super().__init__(Tasktory.CLOSE)


# =============================================================================
# タイムテーブルフィルタ
# =============================================================================

# 特定の日に作業時間が計上されている
class WorkAtDateFilter(TasktoryFilter):
    def __init__(self, date):
        self.test = lambda t: date in self.dates(t)
        return

    def dates(t):
        datetimes = [datetime.fromtimestamp(s) for s, _ in t.timetable]
        return list(set([dt.date() for dt in datetimes]))


# 当日のN日前に作業時間が計上されている
class WorkAtDaysFromTodayFilter(WorkAtDateFilter):
    def __init__(self, n):
        return super().__init__(date.today() - timedelta(n))


# 当日に作業時間が計上されている
class WorkAtTodayFilter(WorkAtDaysFromTodayFilter):
    def __init__(self):
        return super().__init__(0)


# 特定の期間に作業が計上されている
class WorkInPeriodFilter(WorkAtDateFilter):
    def __init__(self, from_date, to_date):
        self.test = lambda t: any([self.in_date(d) for d in self.dates(t)])
        return

    def in_date(self, d):
        return self.from_date <= d and d <= self.to_date


# N日前から当日までに作業が計上されている
class WorkInPeriodToTodayFilter(WorkInPeriodFilter):
    def __init__(self, n):
        today = date.today()
        return super().__init__(today - timedelta(n), today)


# 過去１週間に作業が計上されている
class WorkInWeekFilter(WorkInPeriodToTodayFilter):
    def __init__(self):
        return super().__init__(6)

# =============================================================================
# パスフィルタ
# =============================================================================

# =============================================================================
# タグフィルタ
# =============================================================================
# 特定のタグが付いている

# 特定のタグが付いていない
