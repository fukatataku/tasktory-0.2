# -*- coding: utf-8 -*-

from datetime import date, time, timedelta
from jinja2 import Environment, FileSystemLoader
from lib.common.common import RPRT_DIR


class Report:

    def __init__(self, tmpl_name):
        self.env = Environment(loader=FileSystemLoader(RPRT_DIR))
        self.template = self.env.get_template(tmpl_name)

    def test(self, root):
        return self.template.render(
                date=date, time=time, timedelta=timedelta,
                root=root)
