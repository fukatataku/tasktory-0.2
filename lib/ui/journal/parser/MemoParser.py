#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        return [{'PATH': p, 'TEXT': t} for p, t in zip(paths, texts)]
