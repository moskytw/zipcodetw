#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uniout
import csv
import re
from pprint import pprint

addr_token_re = re.compile(u'''
    (?P<name>.+?)
    (?P<unit>[縣市鄉鎮市區村里路街巷弄號樓])
''', re.X)

addr_str = u'臺北市信義區市府路1號'
print addr_str

addr_tokens = tuple(addr_token_re.findall(addr_str))
print addr_tokens

rule_token_re = re.compile(u'''
    (?P<special>[單雙至]|以下|以上)
    |
    (?P<number>[\d之]+?)
    (?P<unit>[巷弄號樓]|附號)
''', re.X)

#test_cases = [
#    u'全', u'單全',
#    u'雙48號以下', u'雙50號以上',
#    u'7號',
#    u'連2之4號以上',
#    u'14號含附號', u'14巷全',
#    u'47號', u'47附號全',
#    u'雙68巷至70號含附號全',
#    u'連49號含附號以下',
#    u'1之3號及以上附號',
#]
#
#for test_case in test_cases:
#    print test_case
#    print rule_token_re.findall(test_case)
#
#import sys; sys.exit()

def find_unit(tokens, unit, idx=0):

    len_rule_tokens = len(rule_tokens)

    while idx < len_rule_tokens:
        if tokens[idx][-1] != unit:
            idx += 1
        else:
            break
    else:
        return -1

    return idx

def find_unit_rule(rule_tokens, reverse=False):

    len_rule_tokens = len(rule_tokens)
    idx = reverse*-1

    while -len_rule_tokens <= idx < len_rule_tokens:
        if rule_tokens[idx][0]:
            idx += 1+reverse*-2
        else:
            break
    else:
        return -1

    return idx

def match(addr_tokens, rule_tokens):
    return True

rule_zipcode_pairs = [
    (((u'\u96d9', u'', u''),), u'11060'),
    (((u'', u'1', u'\u865f'),), u'11008'),
    ((
        (u'\u55ae', u'', u''),
        (u'', u'3', u'\u865f'),
        (u'\u81f3', u'', u''),
        (u'', u'43', u'\u865f')
    ), u'11073'),
    (((u'', u'45', u'\u865f'),), u'11001'),
    ((
        (u'\u55ae', u'', u''),
        (u'', u'47', u'\u865f'),
        (u'\u4ee5\u4e0a', u'', u'')
    ), u'11073')
]

rule_tokens = rule_zipcode_pairs[2][0]
print rule_tokens
print match(addr_tokens, rule_tokens)

import sys; sys.exit()

triple_addr_rules_zip = {}

with open('zipcodetw-20140131.csv') as f:

    # skip the title line
    next(f)

    for row in csv.reader(f):

        row = [item.decode('utf-8') for item in row]

        zipcode = row[0]

        triple_addr = tuple(addr_token_re.findall(''.join(row[1:-1])))

        rule_str = row[-1].replace(u' ', u'').replace(u'　', u'')
        rule_tokens = tuple(rule_token_re.findall(rule_str))

        if triple_addr not in triple_addr_rules_zip:
            triple_addr_rules_zip[triple_addr] = [(rule_tokens, zipcode)]
        else:
            triple_addr_rules_zip[triple_addr].append((rule_tokens, zipcode))

print addr_tokens[:3]
rule_zipcode_pairs = triple_addr_rules_zip[addr_tokens[:3]]
pprint(rule_zipcode_pairs)
