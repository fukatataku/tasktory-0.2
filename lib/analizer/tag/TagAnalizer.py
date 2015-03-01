#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ツリー中に同名ノードがあればタグに変換
# /ProjectA/開発
# /ProjectB/開発
#   → 「開発」タグ
# バージョンやリビジョン、その他数列もタグに変換（ノードの深さが同じ？）
# - v, ver, version, [0-9], .-_
# - r, rev, revision, [0-9], .-_
# 特に指定されたものもタグに変換
# - タグ管理ファイル

# 01.要求仕様
# 02-基本仕様
# 03_ST仕様
# 04.機能仕様
# 4.1.機能仕様
# 4.2.機能仕様レビュー
# 05.IT仕様
# 06.詳細仕様
# 07.UT仕様
# 08.製造
# 09.UT
# 10.IT
# 11.ST

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../'))

import re
from os import walk
from os.path import join
from lib.core.Tasktory import Tasktory
from lib.common.common import convolute

class TagAnalizer:

    def __init__(self, config):
        self.r_ver = re.compile(r'^v(er(sion)?)?[.-_0-9]+$')
        self.r_rev = re.compile(r'^r(ev(ision)?)?[.-_0-9]+$')
        self.r_num = re.compile(r'^[.-_0-9]+$')
        self.r_name = re.compile(r'^[.\-_0-9]*(.*)$')

        # 登録タグ
        self.reg_tags = config['Tag']['KEYS'].split(',')
        return

    def analize(self, root):
        # ルートパスからタスクトリ名一覧を取得する
        paths = [(p,n) for p, names, _ in walk(root) for n in names]
        tasknames = [n for p,n in paths if Tasktory.istask(join(p, n))]

        # 番号付き名前分離
        names = [self.r_name.match(n).group(1) for n in tasknames]

        # バージョンタグ
        ver_tags = list(set([n for n in names if self.r_ver.match(n)]))

        # リビジョンタグ
        rev_tags = list(set([n for n in names if self.r_rev.match(n)]))

        # 番号タグ
        num_tags = list(set([n for n in names if self.r_num.match(n)]))

        # 重複タグ
        dup_tags = list(set([n for n in names if names.count(n) > 1]))

        return ver_tags + rev_tags + num_tags + dup_tags + self.reg_tags

if __name__ == '__main__':

    # コンフィグ
    import configparser
    from lib.common.common import MAIN_CONF_FILE
    today = datetime.date.today()
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    root = "/Users/taku/tmp/work"
    ta = TagAnalizer(config)
    tags = ta.analize(root)
    print(tags)
