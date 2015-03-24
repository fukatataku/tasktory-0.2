# -*- coding: utf-8 -*-

import win32con
from lib.monitor.WinMonitor import WinMonitor


class DirectoryMonitor(WinMonitor):

    FLAG_NOTIFY = win32con.FILE_NOTIFY_CHANGE_DIR_NAME
