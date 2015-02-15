#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For test
import sys, os
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

import datetime

class DeadLineBuilder:

    def __init__(self, date, config):
        self.today = date
        self.infstr = config['Journal']['INFSTR']

    def build(self, deadline):
        if deadline == float('inf'):
            return self.infstr
        elif isinstance(deadline, int):
            return str(deadline - self.today.toordinal())
        elif deadline == None:
            return ''
        else:
            raise RuntimeError()

if __name__ == '__main__':
    # コンフィグ
    import configparser
    today = datetime.date.today()
    config_path = path('../../../../res/conf/main.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    dlb = DeadLineBuilder(today, config)
    print('@' + dlb.build(None))
    print('@' + dlb.build(float('inf')))
    print('@' + dlb.build(today.toordinal()+10))
