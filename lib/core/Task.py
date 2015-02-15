# -*- coding: utf-8 -*-

import os

class Task:

    OPEN = 0
    WAIT = 1
    CLOSE = 2

    #==========================================================================
    # コンストラクタ
    #==========================================================================
    def __init__(self, deadline, status, comment):
        # 期日
        self.deadline = deadline
        # ステータス
        self.status = status
        # タイムテーブル（開始エポック秒と作業時間（秒）のタプルのリスト）
        self.timetable = []
        # コメント
        self.comment = comment

    #==========================================================================
    # 比較／テスト
    #==========================================================================
    def __bool__(self):
        return True

    #==========================================================================
    # 参照系
    #==========================================================================
    def total(self):
        """合計作業時間（秒）を返す"""
        return sum(t for _,t in self.timetable)

    def timestamp(self):
        """タイムテーブル中の最大の終了エポック秒を返す"""
        if self.timetable:
            return sum(sorted(self.timetable, key=lambda t:t[0])[-1])
        else:
            return 0

    #==========================================================================
    # 変更系
    #==========================================================================
    def merge(self, other):
        """タスクの差分をマージする"""
        if other.deadline is not None: self.deadline = other.deadline
        if other.status is not None: self.status = other.status
        self.timetable += other.timetable
        self.comment = other.comment
        return

    def punch(self, start, sec):
        """作業時間（開始エポック秒、作業秒数）を追加する"""
        self.timetable.append((start, sec))
        return
