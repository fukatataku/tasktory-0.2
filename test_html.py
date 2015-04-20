#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import configparser

from jinja2 import Environment, FileSystemLoader

from lib.core.Tasktory import Tasktory
from lib.common.common import HTML_DIR
from lib.common.common import MAIN_CONF_FILE

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    # タスク作成
    tasks = Tasktory.restore(config["Main"]["ROOT"])

    # HTML作成準備
    env = Environment(loader=FileSystemLoader(HTML_DIR))
    template = env.get_template("timetable.html")
    path = "/Users/taku/tmp/html/test.html"

    today = datetime.date.today()
    a = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    b = a + datetime.timedelta(1)
    a = int(a.timestamp())
    b = int(b.timestamp())

    # HTML書き出し
    with open(path, "w", encoding="utf-8") as f:
        f.write(template.render(
            today=today,
            tasks=[t for t in tasks if t.at(today)],
            root=config["Main"]["ROOT"],
            a=a,
            b=b))
