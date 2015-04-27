#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date
import configparser
from lib.ui.journal.Journal import Journal
from lib.common.common import MAIN_CONF_FILE

if __name__ == '__main__':
    # read config
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    # create journal manager object
    journal = Journal(config)

    # TEST
    journal.commit()
    journal.checkout(date(2015, 4, 28))
