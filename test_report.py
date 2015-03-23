#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from lib.core.Tasktory import Tasktory
from lib.ui.report.Report import Report
from lib.common.common import MAIN_CONF_FILE

if __name__ == '__main__':
    config = ConfigParser()
    config.read(MAIN_CONF_FILE)

    root = Tasktory.restore(config["Main"]["ROOT"])

    report = Report("weekly.tmpl")
    print(report.test(root))
