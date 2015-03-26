# -*- coding: utf-8 -*-

import datetime
import inspect


class Logger:

    # コンストラクタ
    def __init__(self):
        return

    # ログ作成
    def stamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def classmodule(self, r):
        return "{}.{}".format(self.__class__.__name__, inspect.stack()[r][3])

    def log(self, level, event, msg, r=1):
        return "{} {} {} {} {}".format(
                self.stamp(), level, self.classmodule(r+1), event, msg)

    # 書き込み
    def put(self, logline):
        print(logline)
        return

    # 基本ロギングメソッド
    def debug(self, event, msg, r=1):
        self.put(self.log("DEBUG", event, msg, r+1))
        return

    def info(self, event, msg, r=1):
        self.put(self.log("INFO", event, msg, r+1))
        return

    def warn(self, event, msg, r=1):
        self.put(self.log("WARN", event, msg, r+1))
        return

    def error(self, event, msg, r=1):
        self.put(self.log("ERROR", event, msg, r+1))
        return

    def fatal(self, event, msg, r=1):
        self.put(self.log("FATAL", event, msg, r+1))
        return

    # 抽象ロギングメソッド
    def report(self, msg="-", r=1):
        self.debug("REPORT", msg, r+1)
        return

    def start(self, msg="-", r=1):
        self.info("START", msg, r+1)
        return

    def success(self, msg="-", r=1):
        self.info("SUCCESS", msg, r+1)
        return

    def failure(self, msg="-", r=1):
        self.error("FAILURE", msg, r+1)
        return
