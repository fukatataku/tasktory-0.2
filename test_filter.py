#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date
import configparser
from lib.core.Tasktory import Tasktory
from lib.ui.journal.builder.TaskLineBuilder import TaskLineBuilder
from lib.filter.TasktoryFilter import TasktoryFilter
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import FILT_CONF_FILE


if __name__ == '__main__':
    # read config
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    filt_config = configparser.ConfigParser()
    filt_config.read(FILT_CONF_FILE)

    # today
    today = date.today()

    # TaskLineBuilder
    builder = TaskLineBuilder(today, config)

    root_dir = config['Main']['ROOT']
    root_task = Tasktory.restore(root_dir)
    root_task = [] if root_task is None else root_task

    # Filter test
    filters = TasktoryFilter.get_filter(filt_config['JournalFilter'])

    # show all
    for task in root_task:
        print(builder.build(task))

    # show separator
    print("\n==========\n")

    # show
    tasks = filters.select(root_task)
    for task in tasks:
        print(builder.build(task))
