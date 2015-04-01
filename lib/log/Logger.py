# -*- coding: utf-8 -*-

import os
import datetime
import inspect
from lib.common.common import LOG_DIR
from lib.common.common import LOG_FILE


class Logger:

    # ログ作成
    @classmethod
    def __stamp(cls):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def __qualname(cls, r, caller):
        if caller is None:
            return "{}.{}".format(
                    cls.__name__, inspect.stack()[r][3])
        else:
            return caller.__qualname__

    @classmethod
    def __logline(cls, level, event, msg, r=1, caller=None):
        return "{} {} {} {} {}".format(
                cls.__stamp(), level,
                cls.__qualname(r+1, caller), event, msg).replace("\n", "\\n")

    # 書き込み
    @classmethod
    def __putlog(cls, logline):
        # ログディレクトリを作成する
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)

        # ログを書き出す
        path = datetime.date.today().strftime(LOG_FILE)
        with open(path, "a", encoding="utf-8") as logfile:
            logfile.write(logline + "\n")
        return

    # 基本ロギングメソッド
    @classmethod
    def debug(cls, event, msg, r=1, caller=None):
        cls.__putlog(cls.__logline("DEBUG", event, msg, r+1, caller))
        return

    @classmethod
    def info(cls, event, msg, r=1, caller=None):
        cls.__putlog(cls.__logline("INFO", event, msg, r+1, caller))
        return

    @classmethod
    def warn(cls, event, msg, r=1, caller=None):
        cls.__putlog(cls.__logline("WARN", event, msg, r+1, caller))
        return

    @classmethod
    def error(cls, event, msg, r=1, caller=None):
        cls.__putlog(cls.__logline("ERROR", event, msg, r+1, caller))
        return

    @classmethod
    def fatal(cls, event, msg, r=1, caller=None):
        cls.__putlog(cls.__logline("FATAL", event, msg, r+1, caller))
        return

    # 抽象ロギングメソッド
    @classmethod
    def report(cls, msg="-", r=1, caller=None):
        cls.debug("REPORT", msg, r+1, caller)
        return

    @classmethod
    def start(cls, msg="-", r=1, caller=None):
        cls.info("START", msg, r+1, caller)
        return

    @classmethod
    def end(cls, msg="-", r=1, caller=None):
        cls.info("END", msg, r+1, caller)
        return

    @classmethod
    def dstart(cls, msg="-", r=1, caller=None):
        cls.debug("START", msg, r+1, caller)
        return

    @classmethod
    def dend(cls, msg="-", r=1, caller=None):
        cls.debug("END", msg, r+1, caller)
        return

    @classmethod
    def success(cls, msg="-", r=1, caller=None):
        cls.info("SUCCESS", msg, r+1, caller)
        return

    @classmethod
    def failure(cls, msg="-", r=1, caller=None):
        cls.error("FAILURE", msg, r+1, caller)
        return

    @staticmethod
    def logging(func):
        def wrapper(obj, *args, **kwargs):
            obj.dstart("args={}&kwargs={}".format(args, kwargs), 0, func)
            rtn = func(obj, *args, **kwargs)
            obj.dend("return {}".format(rtn), 0, func)
            return rtn
        return wrapper
