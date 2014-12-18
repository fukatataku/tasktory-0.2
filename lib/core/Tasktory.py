# -*- coding: utf-8 -*-

import os, pickle
from lib.core.Task import Task

class Tasktory(Task):

    PROFILE = '.tasktory'

    #==========================================================================
    # 属性値アクセス
    #==========================================================================
    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key in ('deadline', 'status'): self.sync()
        return

    #==========================================================================
    # コンテナエミュレート
    #==========================================================================
    def __iter__(self):
        """ツリー内の全タスクを走査する"""
        yield self
        for child in self.children():
            for c in child: yield c

    #==========================================================================
    # 変更系
    #==========================================================================
    def sync(self):
        """ファイルシステムに自身を保存する"""
        if not os.path.exists(self.path): os.makedirs(self.path)
        with open(os.path.join(self.path, PROFILE), 'wb') as f:
            pickle.dump(self, f)
        return

    def punch(self, start, sec):
        """作業時間を追加した後、ファイルシステムと同期する"""
        super().punch(start, sec)
        self.sync()
        return

    #==========================================================================
    # ツリー参照系
    #==========================================================================
    def parent(self):
        """親タスクを返す。無ければNoneを返す"""
        return type(self).restore(os.path.dirname(self.path))

    def children(self):
        """子タスクのリストを返す。無ければ空リストを返す"""
        children = [type(self).restore(p) for p in os.listdir(self.path)]
        return [c for c in children if c]

    def level(self):
        """タスクの階層を返す"""
        parent = self.parent()
        return parent.level() + 1 if parent else 0

    #==========================================================================
    # タスク作成系クラスメソッド
    #==========================================================================
    @classmethod
    def new(cls, path, deadline, status):
        """ディレクトリパスを指定してタスクを作成する"""
        # タスクを作成する
        task = cls.__init__(deadline, status)
        task.path = os.path.abspath(path)

        # ファイルシステムと同期する
        task.sync()
        return task

    @classmethod
    def restore(cls, path):
        """ディレクトリパスを指定してタスクを復元する"""
        profile = os.path.join(path, PROFILE)
        if not os.path.isfile(profile): return None
        with open(profile, 'rb') as f:
            task = pickle.load(f)
            task.path = os.path.abspath(path)
            return task
