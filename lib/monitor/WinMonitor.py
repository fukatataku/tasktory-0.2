# -*- coding: utf-8 -*-

import win32file
import win32con
import win32api


class WinMonitor:

    FLAG_SHARE =\
            win32con.FILE_SHARE_READ |\
            win32con.FILE_SHARE_WRITE |\
            win32con.FILE_SHARE_DELETE

    FLAG_NOTIFY = None

    def __init__(self, hwnd, msg, dirpath):

        # 親ウィンドウハンドラ
        self.hwnd = hwnd

        # メッセージ
        self.msg = msg

        # 監視対象ディレクトリのハンドル
        self.hDir = win32file.CreateFile(
                dirpath, 0x0001, self.FLAG_SHARE, None, win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS, None)

        # 開始する
        self.run()

    def run(self):
        while True:
            # ディレクトリに変更があるまでブロックする
            notice = win32file.ReadDirectoryChangesW(
                    self.hDir, 1024, True, self.FLAG_NOTIFY, None, None)

            # 通知する
            self.inform(notice)

    def inform(self, notice):
        win32api.SendMessage(self.hwnd, self.msg, None, None)
