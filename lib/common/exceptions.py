# -*- coding: utf-8 -*-


class ExceptionMeta(type):

    __num = 0
    __classes = []

    def __new__(cls, name, bases, namespace):
        # 例外IDを付与する
        namespace['ID'] = cls.__num
        cls.__num += 1

        # 例外を作成してリストに追加
        created_class = type.__new__(cls, name, bases, namespace)
        cls.__classes.append(created_class)

        return created_class

    @classmethod
    def classes(cls):
        return cls.__classes


class TasktoryError(Exception, metaclass=ExceptionMeta):
    """タスクトリエラーの基底クラス"""
    MSG = ""


class TasktoryWarning(Warning, metaclass=ExceptionMeta):
    """タスクトリ警告の基底クラス"""
    MSG = ""
