#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.Regexplate import Regexplate


class PathAliasParser:
    """パスエイリアス解析機"""

    def __init__(self, config):
        self.template = Regexplate(config['Journal']['PATHALIAS'])

    def parse(self, string):
        return self.template.parse(string)

    def match(self, string):
        return self.template.match(string)
