#!C:/python/python3.4/python
# -*- coding: utf-8 -*-

from datetime import date
import configparser
from multiprocessing import Process
from lib.ui.icon.WinTrayIcon import TrayIcon
from lib.ui.journal.Journal import Journal
from lib.monitor.WinFileMonitor import FileMonitor
from lib.monitor.WinDirectoryMonitor import DirectoryMonitor
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import FILT_CONF_FILE
from lib.common.common import ICON_IMG_FILE
from lib.common.exceptions import TasktoryError
from lib.common.exceptions import TasktoryWarning


class TasktoryIcon(TrayIcon):

    MSG_CHDIR = TrayIcon.MSG_NOTIFY + 1
    MSG_CHFILE = TrayIcon.MSG_NOTIFY + 2

    def __init__(self):
        try:
            # コンフィグ
            config = configparser.ConfigParser()
            config.read(MAIN_CONF_FILE)
            filt_config = configparser.ConfigParser()
            filt_config.read(FILT_CONF_FILE)

            # ジャーナル
            self.journal = Journal(config, filt_config)
            self.journal.checkout(date.today())

            # ウィンドウプロシージャ
            wp = {
                    self.MSG_CHDIR: self.chdir,
                    self.MSG_CHFILE: self.chfile,
                    }

            # ポップアップメニュー
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

            # 親クラスのコンストラクタ
            super().__init__(wp, ICON_IMG_FILE, menu)

            # モニタープロセス作成
            self.file_monitor = Process(
                    target=FileMonitor,
                    args=(
                        self.hwnd,
                        self.MSG_CHFILE,
                        config["Main"]["JOURNAL"]))
            self.dir_monitor = Process(
                    target=DirectoryMonitor,
                    args=(
                        self.hwnd,
                        self.MSG_CHDIR,
                        config["Main"]["ROOT"]))

            # モニタープロセス開始
            self.file_monitor.start()
            self.dir_monitor.start()

            # メッセージループ開始
            self.run()
        except TasktoryError as e:
            self.popup("ERROR", str(e))
        except TasktoryWarning as e:
            self.popup("WARNING", str(e))
        except:
            self.popup("FATAL", str(e))
        return

    def command(self, hwnd, msg, wparam, lparam):
        print(hwnd, msg, wparam, lparam)
        if wparam == 0:
            self.sync()
        elif wparam == 4:
            self.destroy()
        return

    def destroy(self):
        self.file_monitor.terminate()
        self.dir_monitor.terminate()
        super().destroy()
        return

    def sync(self):
        try:
            self.journal.commit()
            self.journal.checkout(date.today())
            self.popup("INFO", "System Synchronized")
        except TasktoryError as e:
            self.popup("ERROR", str(e))
        except TasktoryWarning as e:
            self.popup("WARNING", str(e))
        except:
            self.popup("FATAL", str(e))
        return

    def chdir(self, hwnd, msg, wparam, lparam):
        try:
            self.journal.checkout(date.today())
            self.popup("INFO", "FileSystem updated.")
        except TasktoryError as e:
            self.popup("ERROR", str(e))
        except TasktoryWarning as e:
            self.popup("WARNING", str(e))
        except:
            self.popup("FATAL", str(e))
        return

    def chfile(self, hwnd, msg, wparam, lparam):
        try:
            self.journal.commit()
            self.popup("INFO", "Journal updated.")
        except TasktoryError as e:
            self.popup("ERROR", str(e))
        except TasktoryWarning as e:
            self.popup("WARNING", str(e))
        except:
            self.popup("FATAL", str(e))
        return
