#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from lib.ui.journal.Journal import Journal
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import FILT_CONF_FILE

if __name__ == '__main__':
    # read config
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    filt_config = configparser.ConfigParser()
    filt_config.read(FILT_CONF_FILE)

    # create journal manager object
    journal = Journal(config, filt_config)

    # TEST
    journal.commit()
    journal.checkout()
