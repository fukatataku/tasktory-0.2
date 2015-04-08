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
    def __str__(self):
        return self.MSG

    def __repr__(self):
        return self.__str__()


class TasktoryWarning(Warning, metaclass=ExceptionMeta):
    """タスクトリ警告の基底クラス"""
    def __str__(self):
        return self.MSG

    def __repr__(self):
        return self.__str__()


# =============================================================================
# Journal関係
# =============================================================================
class JournalBuilderDeadLineValueError(TasktoryError):
    MSG = "期日の値が不正です"


class JournalParserNoMatchTemplateError(TasktoryError):
    MSG = "ジャーナルがテンプレートに一致しません"


class JournalParserCommentFormatError(TasktoryError):
    MSG = "コメントのフォーマットが不正です"


class JournalParserDuplicateTaskError(TasktoryError):
    MSG = "タスクトリに重複があります"


class JournalParserOverlapTimeTableError(TasktoryError):
    MSG = "作業時間に重複があります"


class JournalManagerNoExistTaskOfMemoError(TasktoryError):
    MSG = "存在しないタスクのメモが記載されています"


# =============================================================================
# TrayIcon関係
# =============================================================================
class TrayIconPopupMenuError(TasktoryError):
    MSG = "ポップアップメニューに不明な項目が含まれています"


class UnknownError(TasktoryError):
    MSG = "何かに失敗しました"
