#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

import os
from datetime import date
import configparser
from multiprocessing import Process
import win32api
from lib.ui.icon.WinTrayIcon import TrayIcon
from lib.ui.journal.Journal import Journal
from lib.monitor.WinFileMonitor import FileMonitor
from lib.monitor.WinDirectoryMonitor import DirectoryMonitor
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import FILT_CONF_FILE
from lib.common.common import ICON_IMG_FILE
from lib.common.exceptions import TasktoryError
from lib.common.exceptions import TasktoryWarning
from lib.log.Logger import Logger


class TasktoryIcon(TrayIcon):

    MSG_CHDIR = TrayIcon.MSG_NOTIFY + 1
    MSG_CHFILE = TrayIcon.MSG_NOTIFY + 2
    MSG_UNLOCK = TrayIcon.MSG_NOTIFY + 3

    # 例外処理デコレータ
    def exception(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except TasktoryError as e:
                self.popup("ERROR", "MESSAGE: {}".format(str(e)))
                self.error("ERROR", str(e))
            except TasktoryWarning as e:
                self.popup("WARNING", "MESSAGE: {}".format(str(e)))
                self.warn("WARNING", str(e))
            except Exception as e:
                self.popup("FATAL", "MESSAGE: {}".format(str(e)))
                self.fatal("FATAL", str(e))
        return wrapper

    # 排他制御デコレータ
    def exclusion(func):
        def wrapper(self, *args, **kwds):
            if self.islock():
                return False
            self.lock()
            func(self, *args, **kwds)
            self.unlock()
            return True
        return wrapper

    def __init__(self):
        # 排他制御
        self.__lock = False

        # ウィンドウプロシージャ
        wp = {
                self.MSG_CHDIR: self.chdir,
                self.MSG_CHFILE: self.chfile,
                self.MSG_UNLOCK: self.__unlock,
                }

        # ポップアップメニュー
        menu = [
                ('Sync', 0),
                ('Report', [
                    ('ALL', 1),
                    ('チーム週報', 2),
                    ('チーム月報', 3),
                    ]),
                (None, None),
                ('Quit', 4),
                ]

        self.proc = {
                0: self.sync,
                1: self.dummy,
                2: self.dummy,
                3: self.dummy,
                4: self.destroy,
                }

        # 親クラスのコンストラクタ
        super().__init__(wp, ICON_IMG_FILE, menu)

        # コンフィグ
        config = configparser.ConfigParser()
        config.read(MAIN_CONF_FILE)
        filt_config = configparser.ConfigParser()
        filt_config.read(FILT_CONF_FILE)

        # ディレクトリを作成する
        root_dir = config["Main"]["ROOT"]
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)

        # ジャーナル
        self.journal = Journal(config, filt_config)
        self.journal.checkout(date.today())

        # モニタープロセス作成
        self.file_monitor = Process(
                target=FileMonitor,
                args=(
                    self.hwnd,
                    self.MSG_CHFILE,
                    config["Main"]["JOURNAL"]))
        self.dir_monitor = Process(
                target=DirectoryMonitor,
                args=(
                    self.hwnd,
                    self.MSG_CHDIR,
                    config["Main"]["ROOT"]))

        # モニタープロセス開始
        self.file_monitor.start()
        self.dir_monitor.start()

        # メッセージループ開始
        self.run()
        return

    @Logger.logging
    def command(self, hwnd, msg, wparam, lparam):
        return self.proc[wparam]()

    @Logger.logging
    def dummy(self):
        return

    @Logger.logging
    def destroy(self):
        self.file_monitor.terminate()
        self.dir_monitor.terminate()
        super().destroy()
        return

    @exception
    @exclusion
    @Logger.logging
    def sync(self):
        self.journal.commit()
        self.journal.checkout(date.today())
        self.popup("INFO", "ジャーナルとファイルシステムを同期しました")
        return

    @exception
    @exclusion
    @Logger.logging
    def chdir(self, hwnd, msg, wparam, lparam):
        self.journal.checkout(date.today())
        self.popup("INFO", "ジャーナルを更新しました")
        return

    @exception
    @exclusion
    @Logger.logging
    def chfile(self, hwnd, msg, wparam, lparam):
        t, m = self.journal.commit()
        self.popup(
            "INFO",
            "{}個のタスクと{}個のメモをコミットしました".format(t, m))
        return

    @Logger.logging
    def islock(self):
        return self.__lock

    @Logger.logging
    def lock(self):
        self.__lock = True
        return

    @Logger.logging
    def unlock(self):
        win32api.SendMessage(self.hwnd, self.MSG_UNLOCK, None, None)
        return

    @Logger.logging
    def __unlock(self, hwnd, msg, wparam, lparam):
        self.__lock = False
        return
