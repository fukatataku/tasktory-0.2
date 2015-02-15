#!python3
# -*- coding: utf-8 -*-

import re
from string import Template

# %(%Y年%)%M月%D日(%W)%R%%
# %Y年%M月%D日(%W)%R%%
# ((?P<Y>.*)年)?(?P<M>.*)月(?P<D>.*)日/((?P<W>.*)/)(?P<R>.*)%

class Regexplate(Template):

    delimiter = '%'

    # Regex of placeholder
    esc = re.compile(r'([.^$*+?{}\\\[\]|()])')
    ph = re.compile(r'%(\\\{)?([a-zA-Z0-9_]+)(?(1)\\\})')

    def __init__(self, template):
        # Write Template
        wtmpl = template
        wtmpl = self.__esc(wtmpl, lambda s:s.replace('%(','').replace('%)',''))
        super().__init__(wtmpl)

        # Capture Regex
        creg = template
        creg = self.__esc(creg, lambda s:self.esc.sub(r'\\\1', s))
        creg = self.__esc(creg, lambda s:self.ph.sub(r'(?P<\2>.*?)', s))
        creg = self.__esc(creg, lambda s:s.replace('%\\(', '('))
        creg = self.__esc(creg, lambda s:s.replace('%\\)', ')?'))
        creg = '%'.join(creg.split('%%'))
        self.creg = re.compile(r'\A' + creg + r'\Z', re.S)

        # No Capture Regex
        ncreg = template
        ncreg = self.__esc(ncreg, lambda s:self.esc.sub(r'\\\1', s))
        ncreg = self.__esc(ncreg, lambda s:self.ph.sub(r'(?:.*)', s))
        ncreg = self.__esc(ncreg, lambda s:s.replace('%\\(', '(?:'))
        ncreg = self.__esc(ncreg, lambda s:s.replace('%\\)', ')?'))
        self.ncreg = re.compile(ncreg, re.M)

    @staticmethod
    def __esc(string, proc):
        return '%%'.join([proc(s) for s in string.split('%%')])

    def parse(self, string):
        m = self.creg.match(string)
        if not m: raise ValueError()
        return m.groupdict()

    def match(self, string):
        m = self.creg.match(string)
        return True if m else False

    def split(self, string):
        return self.ncreg.split(string)

    def findall(self, string):
        return self.ncreg.findall(string)

if __name__ == '__main__':
    tmpl = Regexplate("%(%Y年%)%{M}月%D日")
    d = {'Y': 2014, 'M': 12, 'D': 27}
    print(tmpl.template)
    print(tmpl.substitute(d))
    print(tmpl.parse('2015年1月6日'))
    print(tmpl.parse('1月6日'))

    print(tmpl.creg.pattern)
    print(tmpl.ncreg.pattern)

    text = """
2015年1月7日
hogehoge
2015年1月8日
fugafuga
1月9日
piyopiyo
"""
    print(tmpl.split(text))
    print(tmpl.findall(text))

    tmpl = Regexplate("## %Y/%m/%d %H:%M")
    text = """
## 2015/1/7 10:20
hogehoge
## 2015/1/8 11:30
fugafuga
## 2015/1/9 12:40
piyopiyo
"""
    print(tmpl.split(text))
    print(tmpl.findall(text))
