# -*- coding: utf-8 -*-

import os
import win32con
from lib.monitor.WinMonitor import WinMonitor


class FileMonitor(WinMonitor):

    FLAG_NOTIFY =\
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |\
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE

    def __init__(self, hwnd, msg, filepath):

        # ファイル名
        self.filename = os.path.basename(filepath)

        super().__init__(hwnd, msg, os.path.dirname(filepath))

    def inform(self, notice):
        # 変更内容を確認して通知する
        for act, path in notice:
            if path == self.filename:
                super().inform(notice)
