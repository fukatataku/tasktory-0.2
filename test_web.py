#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process
from lib.ui.web.web import start

if __name__ == '__main__':
    p = Process(target=start, args=())
    p.start()
    # p.terminate()
