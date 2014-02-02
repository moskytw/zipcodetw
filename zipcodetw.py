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

    @staticmethod
    def get_number_pair(token):
        return (
            int(token[Address.NUMBER]     or 0),
            int(token[Address.SUB_NUMBER] or 0)
        )

    def __init__(self, addr_str):

        self.addr_str = addr_str
        self.tokens = Address.tokenize(addr_str)
        self.first_number_token_idx = 0
        self.number_pair = (0, 0)

        len_tokens = len(self.tokens)
        while self.first_number_token_idx < len_tokens:
            if self.tokens[self.first_number_token_idx][Address.NUMBER]:
                self.number_pair = Address.get_number_pair(self.tokens[self.first_number_token_idx])
                break
            self.first_number_token_idx += 1

    def __repr__(self):
        return 'Address(%r)' % self.addr_str

    def __cmp__(self, other):

        for i in range(self.first_number_token_idx):
            if self.tokens[i] != other.tokens[i]:
                raise ValueError("incompatible")

        return cmp(self.number_pair, other.number_pair)

addr1 = Address('臺北市信義區市府路1號')
print addr1.tokens
addr2 = Address('臺北市信義區市府路2號')
print addr2.tokens
addr3 = Address('臺北市信義區市府路2-1號')
print addr3.tokens
addr4 = Address('臺北市信義區市府路2-5號')
print addr4.tokens
addr5 = Address('臺北市信義區市府路')
print addr5.tokens
addr6 = Address('臺北市信義區另一條路1號')
print addr6.tokens

print addr1 < addr2
print addr2 < addr3
print addr3 < addr4
print addr4 < addr5
#print addr5 < addr6 # ValueError

class AddressRule(Address):

    RULE_TOKEN_RE = re.compile(u'''
        [連全單雙至]
        |
        以下|以上
        |
        含附號|及以上附號|含附號以下
        |
        附號全
    ''', re.X)

    @staticmethod
    def extract_tokens(addr_rule_str):

        if isinstance(addr_rule_str, str):
            addr_rule_str = addr_rule_str.decode('utf-8')

        rule_tokens = []

        def extract_token(m):
            token = m.group()
            rule_tokens.append(token)
            if token == u'附號全':
                return u'號'
            return ''

        addr_str = AddressRule.RULE_TOKEN_RE.sub(extract_token, addr_rule_str)

        return (rule_tokens, addr_str)

    def __init__(self, addr_rule_str):

        self.addr_rule_str = addr_rule_str
        self.rule_tokens, addr_str = AddressRule.extract_tokens(addr_rule_str)
        Address.__init__(self, addr_str)

    def __repr__(self):
        return 'AddressRule(%r)' % self.addr_rule_str

    def match(self, addr):

        try:
            cmp_val = cmp(self, addr)
        except ValueError:
            return False

        if not self.rule_tokens:
            return cmp_val == 0

        print addr.number_pair, self.number_pair

        for rule_token in self.rule_tokens:

            if rule_token == u'單' and not addr.number_pair[0] & 1 == 1:
                return False
            if rule_token == u'雙' and not addr.number_pair[0] & 1 == 0:
                return False
            if u'以上' in rule_token and not addr.number_pair >= self.number_pair:
                return False
            if u'以下' in rule_token and not addr.number_pair <= self.number_pair:
                return False
            if rule_token == u'至' and not self.number_pair <= addr.number_pair <= Address.get_number_pair(self.tokens[self.first_number_token_idx+1]):
                return False

        return True

test_cases = [
    u'全', u'單全',
    u'雙48號以下', u'雙50號以上',
    u'7號',
    u'連2之4號以上',
    u'14號含附號', u'14巷全',
    u'47號', u'47附號全',
    u'雙68巷至70號含附號全',
    u'連49號含附號以下',
    u'1之3號及以上附號',
]

for test_case in test_cases:
    addr_rule_str = u'臺北市信義區市府路'+test_case
    addr_rule = AddressRule(addr_rule_str)
    print addr_rule
    print addr_rule.tokens
    print addr_rule.rule_tokens
    print

addr_rule = AddressRule('臺北市信義區市府路14巷全')
print addr_rule
print addr_rule.tokens
print addr_rule.rule_tokens
print addr_rule.match(Address('臺北市信義區市府路14巷3號'))

import sys; sys.exit()

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
