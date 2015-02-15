#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.common.Regexplate import Regexplate

class PathAliasParser:
    """パスエイリアス解析機"""

    def __init__(self, config):
        self.template = Regexplate(config['Journal']['PATHALIAS'])

    def parse(self, string):
        return self.template.parse(string)

    def match(self, string):
        return self.template.match(string)

if __name__ == '__main__':
    # コンフィグ
    import configparser
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    pap = PathAliasParser(config)
    print(pap.parse('[]'))
    print(pap.parse('[/path/to/alias]'))
