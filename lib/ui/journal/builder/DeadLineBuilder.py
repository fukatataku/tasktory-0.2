#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class DeadLineBuilder:

    def __init__(self, date, config):
        self.today = date
        self.infstr = config['Journal']['INFSTR']

    def build(self, deadline):
        if deadline == float('inf'):
            return self.infstr
        elif isinstance(deadline, int):
            return str(deadline - self.today.toordinal())
        elif deadline is None:
            return ''
        else:
            raise RuntimeError()
