#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date
import configparser
from lib.ui.journal.JournalManager import JournalManager
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import FILT_CONF_FILE

if __name__ == '__main__':
    # read config
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    filt_config = configparser.ConfigParser()
    filt_config.read(FILT_CONF_FILE)

    # prepare date infomation
    today = date.today()

    # create journal manager object
    jm = JournalManager(config, filt_config)

    journal = jm.load(today)
    jm.write(journal)
    # journal = jm.read()
    # jm.save(journal)
