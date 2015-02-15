# -*- coding: utf-8 -*-

class CommentBuilder:
    """コメント構築器"""

    def __init__(self):
        return

    def build(self, comment):
        return ' # {}'.format(comment) if comment else ''

if __name__ == '__main__':
    cb = CommentBuilder()

    print(cb.build('hogehoge'))
