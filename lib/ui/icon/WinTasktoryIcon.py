#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

from lib.ui.icon.WinTrayIcon import TrayIcon
from lib.common.common import ICON_IMG_FILE


class TasktoryIcon(TrayIcon):

    def __init__(self):
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

        # 親クラスのコンストラクタ
        super().__init__(ICON_IMG_FILE, menu)

        return

    def command(self, hwnd, msg, wparam, lparam):
        print(hwnd, msg, wparam, lparam)
        if wparam == 0:
            self.popup("タイトル", "メッセージ")
        if wparam == 4:
            self.destroy()
        return

    def dummy(self):
        return
