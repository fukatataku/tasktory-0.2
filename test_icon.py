# -*- coding: utf-8 -*-

from multiprocessing import Process, Pipe
import win32api
from lib.ui.icon.WinTasktoryIcon import TasktoryIcon

if __name__ == '__main__':
    # アイコン画像
    imgfile = ""

    # メニュー
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

    # ポップアップメッセージ
    msg = {
            0:  '作業時間の重複',
            1:  '同名のタスクトリ',
            2:  'ファイルシステムに書き出し開始',
            3:  'ファイルシステムに書き出し完了',
            4:  'ジャーナルに書き出し開始',
            5:  'ジャーナルに書き出し完了',
            }

    # パイプ
    conn1, conn2 = Pipe()

    # プロセス作成
    p = Process(target=TasktoryIcon, args=(conn2, imgfile, menu, msg))
    p.start()
    hwnd = conn1.recv()[1]

    # Run
    while True:
        ret = conn1.recv()
        print(ret)
        win32api.SendMessage(hwnd, TasktoryIcon.MSG_DESTROY, None, None)
        break

    p.join()
    conn1.close()
    conn2.close()
