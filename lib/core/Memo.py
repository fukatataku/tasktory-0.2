#!python3
# -*- coding: utf-8 -*-

import os
import re
from lib.common.Regexplate import Regexplate


class Memo:

    stamp = Regexplate('## Written at %Y/%m/%d %H:%M')

    head_blank_reg = re.compile(r'^\n*')
    tail_blank_reg = re.compile(r'\n*$')
    body_blank_reg = re.compile(r'\n{3,}')

    # コンストラクタ
    def __init__(self, dirpath, filename):
        self.dirpath = dirpath
        self.filepath = os.path.join(dirpath, filename)

    # メモ取得
    def get(self):
        # ファイルが無ければ空リストを返す
        if not os.path.isdir(self.dirpath):
            return []
        if not os.path.isfile(self.filepath):
            return []

        # ファイルを読み込んでテキストリストにして返す
        with open(self.filepath, 'r', encoding='utf-8-sig') as f:
            text = f.read()
        return [s for _, s in type(self).parse(text, type(self).stamp)]

    # メモ追記
    def put(self, timestamp, text):
        # ディレクトリが無ければ作成する
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)
        # 余計な空白行を削除する
        text = type(self).trim(text)
        # 既に記載されていれば無視する
        if text in self.get():
            return False
        # 追記する
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write("{}\n\n{}\n\n".format(
                timestamp.strftime(type(self).stamp.template), text))
        return True

    # 補助メソッド
    @classmethod
    def parse(cls, text, template):
        titles = template.findall(text)
        texts = [cls.trim(s) for s in template.split(text)[1:]]
        return list(zip(titles, texts))

    @classmethod
    def trim(cls, string):
        string = Memo.head_blank_reg.sub('', string)
        string = Memo.tail_blank_reg.sub('', string)
        string = Memo.body_blank_reg.sub(r'\n\n', string)
        return string
