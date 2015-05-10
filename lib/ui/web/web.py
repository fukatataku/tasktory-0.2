# -*- coding: utf-8 -*-

import datetime
import configparser

from bottle import route, redirect, request, run
from jinja2 import Environment, FileSystemLoader

from lib.core.Tasktory import Tasktory
from lib.common.common import MAIN_CONF_FILE
from lib.common.common import HTML_DIR
from lib.common.common import URL_TIMETABLE
from lib.common.common import URL_SYNC


@route(URL_SYNC, method="post")
def sync():
    print("=== TEST ===")
    print(request.json)
    return


@route(URL_TIMETABLE)
def timetable():

    # クエリが無ければ、クエリを付けてリダイレクト
    if not request.query.date:
        redirect("{}?date={}".format(
            URL_TIMETABLE,
            datetime.date.today().toordinal()
            ))

    # クエリパラメータから日付取得
    date = datetime.date.fromordinal(int(request.query.date))

    # コンフィグ読み込み
    config = configparser.ConfigParser()
    config.read(MAIN_CONF_FILE)

    # タスク復元
    tasks = Tasktory.restore(config["Main"]["ROOT"])

    # HTMLテンプレートを準備する
    env = Environment(loader=FileSystemLoader(HTML_DIR))
    template = env.get_template("timetable.html")

    # テンプレートに渡す変数を用意する
    a = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
    b = a + datetime.timedelta(1)
    a = int(a.timestamp())
    b = int(b.timestamp())

    return template.render(
            path=URL_TIMETABLE,
            today=date,
            tasks=[t for t in tasks if t.at(date)],
            root=config["Main"]["ROOT"],
            a=a,
            b=b
            )


def start():
    run(host="localhost", port=8080, debug=True)
