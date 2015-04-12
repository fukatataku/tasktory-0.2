#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# import configparser
# from lib.ui.journal.Journal import Journal
# from lib.common.common import MAIN_CONF_FILE
# from lib.common.common import FILT_CONF_FILE


def usage():
    print("USAGE:")
    print("journal checkout YYYY MM DD")
    print("journal commit FILEPATH")
    return


def checkout():
    return


def commit():
    return

if __name__ == '__main__':
    # read config
    # config = configparser.ConfigParser()
    # config.read(MAIN_CONF_FILE)

    # filt_config = configparser.ConfigParser()
    # filt_config.read(FILT_CONF_FILE)

    # create journal object
    # journal = Journal()

    argv = sys.argv
    if len(argv) < 2:
        usage()
        sys.exit(1)

    com = sys.argv[1]
    if com == "checkout":
        checkout()

    elif com == "commit":
        commit()
