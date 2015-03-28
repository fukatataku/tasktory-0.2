# -*- coding: utf-8 -*-

from lib.log.Logger import Logger


class CommentBuilder(Logger):
    """コメント構築器"""

    def __init__(self):
        super().__init__()
        return

    @Logger.logging
    def build(self, comment):
        return ' # {}'.format(comment) if comment else ''
