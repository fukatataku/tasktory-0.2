# -*- coding: utf-8 -*-

from lib.ui.icon.WinTasktoryIcon import TasktoryIcon

if __name__ == '__main__':
    # プロセス作成
    icon = TasktoryIcon()

    # Run
    icon.run()
    # win32api.SendMessage(hwnd, TasktoryIcon.MSG_DESTROY, None, None)
