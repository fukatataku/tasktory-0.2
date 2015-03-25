#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

import configparser
from lib.ui.icon.WinTrayIcon import TrayIcon
from lib.ui.journal.Journal import Journal
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import FILT_CONF_FILE
from lib.common.common import ICON_IMG_FILE


class TasktoryIcon(TrayIcon):

    def __init__(self):
        # コンフィグ
        config = configparser.ConfigParser()
        config.read(MAIN_CONF_FILE)
        filt_config = configparser.ConfigParser()
        filt_config.read(FILT_CONF_FILE)

        # ジャーナル
        self.journal = Journal(config, filt_config)

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
