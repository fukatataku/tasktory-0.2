#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

import re

class CommentParser:
    """コメント解析器"""

    reg = re.compile(r'\s*#(.*)')

    def __init__(self):
        return

    def parse(self, string):
        m = self.reg.match(string.strip())
        if not m: raise RuntimeError()
        return {'COMMENT': m.group(1).strip()}

    def match(self, string):
        return isinstance(string, str) and self.reg.match(string)

if __name__ == '__main__':
    cp = CommentParser()

    print(cp.parse('#'))
    print(cp.parse(' # '))
    print(cp.parse(' # HOGEHOGE'))
    print(cp.parse(' # HOGEHOGE '))
