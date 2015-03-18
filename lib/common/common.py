#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join, dirname, abspath

__HERE__ = dirname(abspath(__file__))
__HOME__ = abspath(join(__HERE__, '..', '..'))

RES_DIR = join(__HOME__, 'res')
CONF_DIR = join(RES_DIR, 'conf')
TMPL_DIR = join(RES_DIR, 'template')
RPRT_DIR = join(TMPL_DIR, "report")

MAIN_CONF_FILE = join(CONF_DIR, 'main.conf')
FILT_CONF_FILE = join(CONF_DIR, 'filter.conf')
JRNL_TMPL_FILE = join(TMPL_DIR, 'journal.tmpl')


def convolute(proc, iterable, start=0):
    rtn = []
    acc = start
    for value in iterable:
        result, acc = proc(value, acc)
        rtn.append(result)
    return rtn
