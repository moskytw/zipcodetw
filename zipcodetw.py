#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re

rule_token_re = re.compile(u'''
    (?P<prefix>[全單雙連至])?
    (?P<number>.+?)
    (?P<unit>[巷弄號樓]|附號全)
    (?P<suffix>全|以下|以上|含附號全?|含附號以下|及以上附號)?
''', re.X)

addr_token_re = re.compile(u'''
    (?P<name>.+?)
    (?P<unit>[縣市鄉鎮市區村里路街巷弄號樓])
''', re.X)

counter = 0

with open('zipcodetw-20140131.csv') as f:

    next(f)

    for row in csv.reader(f):

        zipcode = row[0]
        triple_addr = row[1:-1]
        rule_str = row[-1].decode('utf-8').replace(u' ', u'').replace(u'　', u'')
        rule_tokens = rule_token_re.findall(rule_str)
        if len(rule_tokens) != sum(rule_str.count(k) for k in u'巷弄號樓')-(u'附號' in rule_str):
            print rule_str
            print rule_tokens
            print len(rule_tokens)
            counter += 1

print counter

addr_str = u'臺北市信義區市府路1之23號'

print addr_str
print addr_token_re.findall(addr_str)
