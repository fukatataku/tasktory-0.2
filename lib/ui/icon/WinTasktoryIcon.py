#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

import os
from lib.ui.icon.WinTrayIcon import TrayIcon


class TasktoryIcon(TrayIcon):

    def __init__(self, conn, imgfile, menu, msg):
        # 親プロセスとのコネクタ
        self.conn = conn

        # 親クラスのコンストラクタ
        super().__init__(imgfile, menu, msg)

        # 親プロセスにウィンドウハンドルを渡す
        self.conn.send((os.getpid(), self.hwnd, None))

        # メッセージループ
        self.run()
        return

    def command(self, hwnd, msg, wparam, lparam):
        self.conn.send((os.getpid(), wparam, lparam))
        return

    def popup(self, hwnd, msg, wparam, lparam):
        return super().popup(hwnd, msg, wparam, lparam)
