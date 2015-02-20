# -*- coding: utf-8 -*-

import os
import win32api, win32gui, win32con

class TrayIcon:

    TITLE = 'TrayIcon'

    def __init__(self, imgfile):
        # Create window procedure
        self.wp = {
                win32con.WM_DESTROY: self.destroy,
                win32con.WM_COMMAND: self.command,
                }

        # Window class
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = 'TrayIcon'
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map

        # Register window class
        win32gui.RegisterClass(wc)

        # Create Window
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName, '',
                win32con.WS_OVERLAPPED | win32con.WS_SYSMENU, 0, 0,
                win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0,
                wc.hInstance, None)
        win32gui.UpdateWindow(self.hwnd)

        # Create icon
        self.hicon = win32gui.LoadImage(
                wc.hInstance, imgfile, win32con.IMAGE_ICON, 0, 0,
                win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)

        # Add icon into task bar
        flag = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flag, self.MSG_NOTIFY, self.hicon, self.TITLE)
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

        # Create popup menu

    def run(self):
        win32gui.PumpMessages()

    def destroy(self, hwnd, msg, wparam, lparam):
        return

    def command(self, hwnd, msg, wparam, lparam):
        return

