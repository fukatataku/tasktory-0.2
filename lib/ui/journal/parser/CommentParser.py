#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from lib.common.exceptions import JournalParserCommentFormatError


class CommentParser:
    """コメント解析器"""

    reg = re.compile(r'\s*#(.*)')

    def __init__(self):
        return

    def parse(self, string):
        m = self.reg.match(string.strip())
        if not m:
            raise JournalParserCommentFormatError()
        return {'COMMENT': m.group(1).strip()}

    def match(self, string):
        return isinstance(string, str) and self.reg.match(string)
