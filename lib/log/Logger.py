# -*- coding: utf-8 -*-

import datetime
import inspect
from lib.common.common import LOG_FILE


class Logger:

    # コンストラクタ
    def __init__(self):
        import os
        # ログディレクトリを作成する
        from lib.common.common import LOG_DIR
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)

        # ログファイル名を解決する
        self.logfile = datetime.date.today().strftime(LOG_FILE)
        return

    # ログ作成
    def __stamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __qualname(self, r, caller):
        if caller is None:
            return "{}.{}".format(
                    self.__class__.__name__, inspect.stack()[r][3])
        else:
            return caller.__qualname__

    def __logline(self, level, event, msg, r=1, caller=None):
        return "{} {} {} {} {}".format(
                self.__stamp(), level,
                self.__qualname(r+1, caller), event, msg).replace("\n", "\\n")

    # 書き込み
    def __putlog(self, logline):
        with open(self.logfile, "a", encoding="utf-8") as logfile:
            logfile.write(logline + "\n")
        return

    # 基本ロギングメソッド
    def debug(self, event, msg, r=1, caller=None):
        self.__putlog(self.__logline("DEBUG", event, msg, r+1, caller))
        return

    def info(self, event, msg, r=1, caller=None):
        self.__putlog(self.__logline("INFO", event, msg, r+1, caller))
        return

    def warn(self, event, msg, r=1, caller=None):
        self.__putlog(self.__logline("WARN", event, msg, r+1, caller))
        return

    def error(self, event, msg, r=1, caller=None):
        self.__putlog(self.__logline("ERROR", event, msg, r+1, caller))
        return

    def fatal(self, event, msg, r=1, caller=None):
        self.__putlog(self.__logline("FATAL", event, msg, r+1, caller))
        return

    # 抽象ロギングメソッド
    def report(self, msg="-", r=1, caller=None):
        self.debug("REPORT", msg, r+1, caller)
        return

    def start(self, msg="-", r=1, caller=None):
        self.info("START", msg, r+1, caller)
        return

    def end(self, msg="-", r=1, caller=None):
        self.info("END", msg, r+1, caller)
        return

    def success(self, msg="-", r=1, caller=None):
        self.info("SUCCESS", msg, r+1, caller)
        return

    def failure(self, msg="-", r=1, caller=None):
        self.error("FAILURE", msg, r+1, caller)
        return

    @staticmethod
    def logging(func):
        def wrapper(self, *args, **kwargs):
            self.start("args={}&kwargs={}".format(args, kwargs), 0, func)
            rtn = func(self, *args, **kwargs)
            self.end("return {}".format(rtn), 0, func)
            return rtn
        return wrapper
