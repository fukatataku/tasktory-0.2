# -*- coding: utf-8 -*-


class CommentBuilder:
    """コメント構築器"""

    def __init__(self):
        return

    def build(self, comment):
        return ' # {}'.format(comment) if comment else ''
