# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con
from lib.common.exceptions import TrayIconPopupMenuError


class TrayIcon:

    TITLE = 'TrayIcon'

    MSG_NOTIFY = win32con.WM_USER + 20

    # コンストラクタ
    def __init__(self, wp, imgfile, menu):
        # Create window procedure
        wp.update({
            win32con.WM_DESTROY: self.__destroy,
            win32con.WM_COMMAND: self.command,
            self.MSG_NOTIFY: self.__notify,
            })

        # Window class
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = 'TrayIcon'
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = wp

        # Register window class
        win32gui.RegisterClass(wc)

        # Create Window
        self.hwnd = win32gui.CreateWindow(
                wc.lpszClassName, '',
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
        self.menu = win32gui.CreatePopupMenu()
        for text, item in menu:
            self.menu = TrayIcon.create_menu(self.menu, item, text)

    # メッセージループ開始
    def run(self):
        win32gui.PumpMessages()
        return

    # デストラクタ起動
    def destroy(self):
        win32gui.DestroyWindow(self.hwnd)
        return

    # ポップアップメッセージ（MSG_POPUP送信により起動）
    def popup(self, title, message):
        nid = (
                self.hwnd, 0, win32gui.NIF_INFO, self.MSG_NOTIFY,
                self.hicon, 'Message', message, 200, title)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
        return

    # ポップアップメニューの動作定義
    def command(self, hwnd, msg, wparam, lparam):
        return

    # トレイアイコンデストラクタ
    def __destroy(self, hwnd, msg, wparam, lparam):
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (self.hwnd, 0))
        win32gui.PostQuitMessage(0)
        return

    # アイコンに対するクリック動作定義
    def __notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONDOWN:
            pass
        elif lparam == win32con.WM_LBUTTONDBLCLK:
            pass
        elif lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_RBUTTONDOWN:
            pass
        elif lparam == win32con.WM_RBUTTONDBLCLK:
            pass
        return

    # ポップアップメニュー表示
    def show_menu(self):
        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(
                self.menu, win32con.TPM_LEFTALIGN,
                pos[0], pos[1], 0, self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    # ポップアップメニュー作成
    @staticmethod
    def create_menu(menu, item, text):
        # Normal menu
        if isinstance(item, int):
            flag = win32con.MF_STRING

        # Sub menu
        elif isinstance(item, list):
            flag = win32con.MF_POPUP
            sub_menu = win32gui.CreatePopupMenu()
            for s, v in item:
                sub_menu = TrayIcon.create_menu(sub_menu, v, s)
            item = sub_menu

        # Separotor
        elif item is None:
            flag = win32con.MF_SEPARATOR
            item = 0
            text = ''

        else:
            raise TrayIconPopupMenuError()

        win32gui.AppendMenu(menu, flag, item, text)
        return menu
