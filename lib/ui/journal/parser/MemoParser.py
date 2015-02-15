#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.common.Regexplate import Regexplate

class MemoParser:
    """メモ解析器"""
    def __init__(self, config):
        self.root = config['Main']['ROOT']
        self.template = Regexplate(config['Journal']['MEMOTITLE'])
        return

    def parse(self, string):
        texts = self.template.split(string)[1:]
        titles = self.template.findall(string)
        paths = [self.root + self.template.parse(s)['PATH'] for s in titles]
        return [{'PATH':p, 'TEXT':t} for p,t in zip(paths, texts)]

if __name__ == '__main__':
    import configparser
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    mp = MemoParser(config)
    text = """
うごぐげ
## /path/to/task
あいうえお
かきくけこ

## /hoge/fuga/piyo
hogehoge
fugafuga
piyopiyo
"""
    for d in mp.parse(text):
        print(d)
