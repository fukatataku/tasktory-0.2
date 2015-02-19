# -*- coding: utf-8 -*-

from lib.monitor.WinMonitor import WinMonitor

class DirectoryMonitor(WinMonitor):

    FLAG_NOTIFY = win32con.FILE_NOTIFY_CHANGE_DIR_NAME
