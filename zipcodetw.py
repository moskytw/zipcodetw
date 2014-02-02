#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uniout
import csv
import re
from pprint import pprint

class Address(object):

    TOKEN_RE = re.compile(u'''
        (?:
            (?P<number>\d+)
            (?:[之-](?P<sub_number>\d+))?
            |
            (?P<name>.+?)
        )
        (?P<unit>[縣市鄉鎮市區村里路街巷弄號樓])
    ''', re.X)

    NUMBER = 0
    SUB_NUMBER = 1
    NAME = 2
    UNIT = 3

    @staticmethod
    def tokenize(addr_str):
        if isinstance(addr_str, str):
            addr_str = addr_str.decode('utf-8')
        return tuple(Address.TOKEN_RE.findall(addr_str))

    def __init__(self, addr_str):

        self.addr_str = addr_str
        self.tokens = Address.tokenize(addr_str)

        self.number_token_idx = 0
        len_tokens = len(self.tokens)
        while self.number_token_idx < len_tokens:
            if self.tokens[self.number_token_idx][Address.NUMBER]:
                break
            self.number_token_idx += 1
        else:
            self.number_token_idx = None
            return

        self.number = None
        number_str = self.tokens[self.number_token_idx][Address.NUMBER]
        if number_str:
            self.number = int(number_str)

        self.sub_number = None
        sub_number_str = self.tokens[self.number_token_idx][Address.SUB_NUMBER]
        if sub_number_str:
            self.sub_number = int(sub_number_str)

    def __repr__(self):
        return 'Address(%r)' % self.addr_str

    def __cmp__(self, other):

        if len(self.tokens) != len(other.tokens):
            raise ValueError("the lengths must equivalent")

        if self.number_token_idx is None:
            raise ValueError("this address doesn't include number")

        if other.number_token_idx is None:
            raise ValueError("that address doesn't include number")

        if self.number_token_idx != other.number_token_idx:
            raise ValueError('the number tokens are in different positions')

        for i in range(self.number_token_idx):
            if self.tokens[i] != other.tokens[i]:
                raise ValueError('they are not on same road')

        number_diff = self.number - other.number
        if number_diff == 0:
            if self.sub_number is None:
                return -1
            else:
                return self.sub_number - other.sub_number

        return number_diff

addr1 = Address('臺北市信義區市府路1號')
addr2 = Address('臺北市信義區市府路2號')
addr3 = Address('臺北市信義區市府路2-1號')
addr4 = Address('臺北市信義區市府路2-5號')
addr5 = Address('臺北市信義區另一條路1號')

print addr1 < addr2
print addr2 < addr3
print addr3 < addr4
print addr5 == addr1

rule_token_re = re.compile(u'''
    (?P<special>[單雙至]|以下|以上)
    |
    (?P<number>\d+)
    (?:[之-](?P<sub_number>\d+))?
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

#def match(addr_tokens, rule_tokens):
#
#    special_rule_tokens = []
#    unit_rule_tokens = []
#    for rule_token in rule_tokens:
#        if rule_token[0]:
#            special_rule_tokens.append(rule_token)
#        else:
#            unit_rule_tokens.append(rule_token)
#
#    for addr_token, unit_rule_token in zip(addr_tokens[:-1], unit_rule_tokens):
#        if addr_token != unit_rule_token[1:]:
#            return False
#
#    if special_rule_tokens:
#        for special_rule_token in special_rule_tokens:
#            if special_rule_token[0] == u'單' and int(addr_tokens[-1][-2]) & 1 == 1:
#                continue
#            elif special_rule_token[0] == u'雙' and int(addr_tokens[-1][-2]) & 1 == 0:
#                continue
#            elif special_rule_token[0] == u'以上' and int(addr_tokens[-1][-2]) >= int(unit_rule_tokens[-1][-2]):
#                continue
#            elif special_rule_token[0] == u'以下' and int(addr_tokens[-1][-2]) <= int(unit_rule_tokens[-1][-2]):
#                continue
#            elif special_rule_token[0] == u'至' and int(unit_rule_tokens[-2][-2]) <= int(addr_tokens[-1][-2]) <= int(unit_rule_tokens[-1][-2]):
#                continue
#            return False
#        else:
#            return True
#
#    if addr_tokens[-1] != unit_rule_tokens[-1][1:]:
#        return False
#
#    return True
#
#rule_tokens = rule_token_re.findall(u'3巷2號至5號')
#print rule_tokens
#
#addr_tokens = addr_token_re.findall(u'3巷4號')
#print addr_tokens
#
#print match(addr_tokens, rule_tokens)
#
##import sys; sys.exit()
#
#triple_addr_rules_zip = {}
#
#with open('zipcodetw-20140131.csv') as f:
#
#    # skip the title line
#    next(f)
#
#    for row in csv.reader(f):
#
#        row = [item.decode('utf-8') for item in row]
#
#        zipcode = row[0]
#
#        triple_addr = tuple(addr_token_re.findall(''.join(row[1:-1])))
#
#        rule_str = row[-1].replace(u' ', u'').replace(u'　', u'')
#        rule_tokens = tuple(rule_token_re.findall(rule_str))
#
#        if triple_addr not in triple_addr_rules_zip:
#            triple_addr_rules_zip[triple_addr] = [(rule_tokens, zipcode)]
#        else:
#            triple_addr_rules_zip[triple_addr].append((rule_tokens, zipcode))
#
#addr_str = u'臺北市信義區市府路1號'
#print addr_str
#
#addr_tokens = tuple(addr_token_re.findall(addr_str))
#print addr_tokens
#print addr_tokens[:3]
#rule_zipcode_pairs = triple_addr_rules_zip[addr_tokens[:3]]
#pprint(rule_zipcode_pairs)
#for rule, zipcode in rule_zipcode_pairs:
#    if match(addr_tokens[3:], rule):
#        print zipcode
#        break
#else:
#    print 'match nothing'
