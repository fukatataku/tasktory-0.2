# -*- coding: utf-8 -*-

from lib.ui.icon.WinTrayIcon import TrayIcon

class TasktoryIcon(TrayIcon):

    def __init__(self, imgfile, menu, msg):
        super.__init__(imgfile)
        return

    def command(self, hwnd, wparam, lparam):
        return
