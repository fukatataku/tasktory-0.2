#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.common.exceptions import JournalBuilderDeadLineValueError
from lib.log.Logger import Logger


class DeadLineBuilder(Logger):

    def __init__(self, date, config):
        self.today = date
        self.infstr = config['Journal']['INFSTR']

        super().__init__()

    @Logger.logging
    def build(self, deadline):
        if deadline == float('inf'):
            return self.infstr
        elif isinstance(deadline, int):
            return str(deadline - self.today.toordinal())
        elif deadline is None:
            return ''
        else:
            raise JournalBuilderDeadLineValueError()
