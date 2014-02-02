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

def match(addr_tokens, rule_tokens):

    special_rule_tokens = []
    unit_rule_tokens = []
    for rule_token in rule_tokens:
        if rule_token[0]:
            special_rule_tokens.append(rule_token)
        else:
            unit_rule_tokens.append(rule_token)

    for addr_token, unit_rule_token in zip(addr_tokens[:-1], unit_rule_tokens):
        if addr_token != unit_rule_token[1:]:
            break
    else:
        for special_rule_token in special_rule_tokens:
            if special_rule_token[0] == u'單' and int(addr_tokens[-1][-2]) & 1 == 1:
                continue
            elif special_rule_token[0] == u'雙' and int(addr_tokens[-1][-2]) & 1 == 0:
                continue
            elif special_rule_token[0] == u'以上' and int(addr_tokens[-1][-2]) >= int(unit_rule_tokens[-1][-2]):
                continue
            elif special_rule_token[0] == u'以下' and int(addr_tokens[-1][-2]) <= int(unit_rule_tokens[-1][-2]):
                continue
            elif special_rule_token[0] == u'至' and int(unit_rule_tokens[-2][-2]) <= int(addr_tokens[-1][-2]) <= int(unit_rule_tokens[-1][-2]):
                continue
            break
        else:
            return True

    return False

rule_tokens = rule_token_re.findall(u'3巷1號至10號')
print rule_tokens

addr_tokens = addr_token_re.findall(u'3巷3號')
print addr_tokens

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

addr_str = u'臺北市信義區市府路1號'
print addr_str

addr_tokens = tuple(addr_token_re.findall(addr_str))
print addr_tokens
print addr_tokens[:3]
rule_zipcode_pairs = triple_addr_rules_zip[addr_tokens[:3]]
pprint(rule_zipcode_pairs)
