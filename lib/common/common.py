#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

__HERE__ = os.path.dirname(os.path.abspath(__file__))
__HOME__ = os.path.abspath(os.path.join(__HERE__, '..', '..'))

RES_DIR = os.path.join(__HOME__, 'res')
CONF_DIR = os.path.join(RES_DIR, 'conf')
TMPL_DIR = os.path.join(RES_DIR, 'template')

MAIN_CONF_FILE = os.path.join(CONF_DIR, 'main.conf')
JRNL_TMPL_FILE = os.path.join(TMPL_DIR, 'journal.tmpl')

def convolute(proc, iterable, start=0):
    rtn = []
    acc = start
    for value in iterable:
        result, acc = proc(value, acc)
        rtn.append(result)
    return rtn

