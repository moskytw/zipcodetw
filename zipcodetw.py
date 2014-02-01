#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re

addr_token_re = re.compile(u'''
    (?P<name>.+?)
    (?P<unit>[縣市鄉鎮市區村里路街巷弄號樓])
''', re.X)

rule_token_re = re.compile(u'''
    (?P<special>[單雙連至]|全|以下|以上|含附號全?|含附號以下|及以上附號)
    |
    (?P<number>[\d之]+?)
    (?P<unit>[巷弄號樓]|附號全)
''', re.X)

#test_cases = [
#]
#
#for test_case in test_cases:
#    print test_case
#    print rule_token_re.findall(test_case)
#
#import sys; sys.exit()

triple_addr_rules_zip = {}

with open('zipcodetw-20140131.csv') as f:

    # skip the title line
    next(f)

    for row in csv.reader(f):

        row = [item.decode('utf-8') for item in row]

        zipcode = row[0]

        triple_addr = tuple(addr_token_re.findall(''.join(row[1:-1])))

        rule_str = row[-1].replace(u' ', u'').replace(u'　', u'')
        rule_tokens = rule_token_re.findall(rule_str)

        if triple_addr not in triple_addr_rules_zip:
            triple_addr_rules_zip[triple_addr] = ([rule_tokens], [zipcode])
        else:
            triple_addr_rules_zip[triple_addr][0].append(rule_tokens)
            triple_addr_rules_zip[triple_addr][1].append(zipcode)

# test addr_token_re

import uniout
from pprint import pprint

addr_str = u'臺北市信義區市府路1之23號'
print addr_str
addr_tokens = tuple(addr_token_re.findall(addr_str))
print addr_tokens
print addr_tokens[:3]
pprint(triple_addr_rules_zip[addr_tokens[:3]])
