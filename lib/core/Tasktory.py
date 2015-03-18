# -*- coding: utf-8 -*-

import os
import pickle
from lib.core.Task import Task
from lib.core.Memo import Memo


class Tasktory(Task):

    PROFILE = '.tasktory'
    MEMO = 'memo.txt'

    # コンストラクタ
    def __init__(self, path, deadline, status, comment):
        # タスクを作成する
        super().__init__(deadline, status, comment)
        self.path = path
        self.memo = Memo(path, type(self).MEMO)

    # コンテナエミュレート
    def __iter__(self):
        """ツリー内の全タスクを走査する"""
        yield self
        for child in self.children():
            for c in child:
                yield c

    # 変更系
    def sync(self):
        """ファイルシステムに自身を保存する"""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.PROFILE), 'wb') as f:
            pickle.dump(self, f)
        return self

    def merge(self, other):
        """タスクの差分をマージする"""
        super().merge(other)
        self.sync()
        return self

    # ツリー参照系
    def parent(self):
        """親タスクを返す。無ければNoneを返す"""
        return type(self).restore(os.path.dirname(self.path))

    def children(self):
        """子タスクのリストを返す。無ければ空リストを返す"""
        children = [
            self.restore(self.path + '/' + p) for p in os.listdir(self.path)]
        return [c for c in children if c]

    def level(self):
        """タスクの階層を返す"""
        parent = self.parent()
        return parent.level() + 1 if parent else 0

    # タスク作成系クラスメソッド
    @classmethod
    def new(cls, path, deadline, status, comment):
        """"""
        task = cls(path, deadline, status)
        task.sync()
        return task

    @classmethod
    def restore(cls, path):
        """ディレクトリパスを指定してタスクを復元する"""
        if not cls.istask(path):
            return None
        with open(os.path.join(path, cls.PROFILE), 'rb') as f:
            task = pickle.load(f)
            task.path = os.path.abspath(path)
            return task

    # 参照系クラスメソッド
    @classmethod
    def istask(cls, path):
        """指定したディレクトリがタスクトリかどうか判定する"""
        if not os.path.isdir(path):
            return False
        return os.path.isfile(os.path.join(path, cls.PROFILE))
