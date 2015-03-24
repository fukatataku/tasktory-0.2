# -*- coding: utf-8 -*-

import os
import win32file
import win32con


class WinMonitor:

    FLAG_SHARE =\
            win32con.FILE_SHARE_READ |\
            win32con.FILE_SHARE_WRITE |\
            win32con.FILE_SHARE_DELETE

    FLAG_NOTIFY = None

    def __init__(self, dirpath, conn):

        # プロセスID
        self.pid = os.getpid()

        # 親プロセスとの通信用コネクタ
        self.conn = conn

        # 監視対象ディレクトリのハンドル
        self.hDir = win32file.CreateFile(
                dirpath, 0x0001, self.FLAG_SHARE, None, win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS, None)

    def run(self):
        while True:
            # ディレクトリに変更があるまでブロックする
            notice = win32file.ReadDirectoryChangesW(
                    self.hDir, 2014, True, self.FLAG_NOTIFY, None, None)

            # 通知する
            self.inform(notice)

    def inform(self, notice):
        self.conn((self.pid, None))
