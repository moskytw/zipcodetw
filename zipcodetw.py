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

fail_count = 0

with open('zipcodetw-20140131.csv') as f:

    # skip the title line
    next(f)

    for row in csv.reader(f):

        row = [item.decode('utf-8') for item in row]

        zipcode = row[0]
        triple_addr = row[1:-1]
        rule_str = row[-1].replace(u' ', u'').replace(u'　', u'')

        rule_tokens = rule_token_re.findall(rule_str)

        # check the rule_token_re is right
        if len(rule_tokens) != (
            sum(rule_str.count(k) for k in u'巷弄號樓')
            -(u'附號'     in rule_str) # 5號含附號
            +(u'附號全'   in rule_str) # 86附號全
            -(u'含附號全' in rule_str) # 連68號至69號含附號全
        ):

            print rule_str
            print rule_tokens
            print len(rule_tokens)
            fail_count += 1

print fail_count

# test addr_token_re

addr_token_re = re.compile(u'''
    (?P<name>.+?)
    (?P<unit>[縣市鄉鎮市區村里路街巷弄號樓])
''', re.X)

addr_str = u'臺北市信義區市府路1之23號'

print addr_str
print addr_token_re.findall(addr_str)
