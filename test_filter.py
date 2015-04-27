#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import configparser
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.TaskLineBuilder import TaskLineBuilder
from lib.ui.journal.tester.JournalTester import JournalTester
from lib.common.common import MAIN_CONF_FILE


if __name__ == '__main__':
    # read config
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    # today
    date = datetime.date.today() - datetime.timedelta(2)

    # TaskLineBuilder
    builder = TaskLineBuilder(date, config)

    root_dir = config['Main']['ROOT']
    root_task = Tasktory.restore(root_dir)
    root_task = [] if root_task is None else root_task

    # Filter test
    tester = JournalTester()
    tester.date = date

    # show all
    for task in root_task:
        print(builder.build(task), task.status)

    # show separator
    print("\n==========\n")

    # show
    for task in [t for t in root_task if tester.test(t)]:
        print(builder.build(task))
