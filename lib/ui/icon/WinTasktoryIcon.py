#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

# For test
import sys, os
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../'))

import win32api
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

if __name__ == '__main__':
    from multiprocessing import Process, Pipe
    import os, time

    # アイコンのパス
    #imgfile = 'C:/home/fukata/tmp/1814.png'
    imgfile = 'C:/home/fukata/dev/tasktory/resource/tasktory.ico'

    # ポップアップメッセージ
    msg = {
            0 :  '作業時間の重複',
            1 :  '同名のタスクトリ',
            2 :  'ファイルシステムに書き出し開始',
            3 :  'ファイルシステムに書き出し完了',
            4 :  'ジャーナルに書き出し開始',
            5 :  'ジャーナルに書き出し完了',
            }

    # レポート
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

    conn1, conn2 = Pipe()
    p = Process(target=TasktoryIcon,
            args=(conn2, imgfile, msg, menu))
    p.start()
    hwnd = conn1.recv()[1]

    while True:
        ret = conn1.recv()
        print(ret)
        win32api.SendMessage(hwnd, TrayIcon.MSG_POPUP, 0, 0)
        if ret[1] == 4:
            print('終了します')
            win32api.SendMessage(hwnd, TrayIcon.MSG_DESTROY, None, None)
            break

    p.join()
    conn1.close()
    conn2.close()
    pass

