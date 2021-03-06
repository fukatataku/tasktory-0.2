#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join, dirname, abspath

__HERE__ = dirname(abspath(__file__))
__HOME__ = abspath(join(__HERE__, '..', '..'))

RES_DIR = join(__HOME__, 'res')
CONF_DIR = join(RES_DIR, 'conf')
TMPL_DIR = join(RES_DIR, 'template')
HTML_DIR = join(TMPL_DIR, "html")
RPRT_DIR = join(TMPL_DIR, "report")
LOG_DIR = join(__HOME__, "log")

MAIN_CONF_FILE = join(CONF_DIR, 'main.conf')
JRNL_TMPL_FILE = join(TMPL_DIR, 'journal.tmpl')
ICON_IMG_FILE = join(RES_DIR, "image", "tasktory.ico")
LOG_FILE = join(LOG_DIR, "tasktory.%Y-%m-%d.log")

LOG_LEVEL = 0   # DEBUG
# LOG_LEVEL = 1   # INFO

# URL Mapping
URL_TIMETABLE = "/tasktory/timetable"
URL_SYNC = "/tasktory/sync"


def convolute(proc, iterable, start=0):
    rtn = []
    acc = start
    for value in iterable:
        result, acc = proc(value, acc)
        rtn.append(result)
    return rtn


def unique(iterable, func=lambda v: v):
    rtn = []
    frtn = []
    for v in iterable:
        fv = func(v)
        if fv not in frtn:
            rtn.append(v)
            frtn.append(fv)
    return rtn
