#C:/python/python3.4/python
# -*- coding: utf-8 -*-

# For test
import sys, os, datetime
path = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))
sys.path.append(path('../../../../'))

from lib.common.common import convolute
from lib.core.Tasktory import Tasktory

class TasktoryBuilder:
    """ジャーナル解析結果からタスクトリインスタンスを作成する"""

    def __init__(self, config):
        self.root = config['Main']['ROOT']
        return

    def build(self, attrs):
        names = attrs['PATH'].split('/')
        paths = convolute(lambda p,a: (a+'/'+p,)*2, names[1:], names[0])
        tasks = [self.node(p, attrs) for p in paths]
        return tasks[-1], tasks[:-1]

    def node(self, path, attrs):
        return self.leaf(attrs) if path == attrs['PATH']\
                else self.inner(path, attrs)

    def inner(self, path, attrs):
        return Tasktory(self.root + path, attrs['DEADLINE'], Tasktory.OPEN, '')

    def leaf(self, attrs):
        task = Tasktory(self.root + attrs['PATH'],
                attrs['DEADLINE'], attrs['STATUS'], attrs['COMMENT'])
        for start,sec in attrs['TIMETABLE']: task.punch(start, sec)
        return task

if __name__ == '__main__':
    # コンフィグ
    import configparser
    from lib.common.common import MAIN_CONF_FILE
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    attrs = {'PATH': '/path/to/task', 'DEADLINE': 123456, 'STATUS': 0,
            'COMMENT': 'HOGE', 'TIMETABLE': []}

    tb = TasktoryBuilder(config)
    leaf, inners = tb.build(attrs)
    print('"'+leaf.path+'"')
    print([n.path for n in inners])
