#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'

import re

class Address(object):

    TOKEN_RE = re.compile(u'''
        (?:
            (?P<no>\d+)
            (?:[之-](?P<subno>\d+))?
            (?=[巷弄號樓])
            |
            (?P<name>.+?)
        )
        (?:
            (?P<unit>[縣市鄉鎮市區村里路段街巷弄號樓])
            |
            (?=\d+(?:[之-]\d+)?[巷弄號樓]|$)
        )
    ''', re.X)

    NO    = 0
    SUBNO = 1
    NAME  = 2
    UNIT  = 3

    PAIRS_TO_NORMALIZE = (
        # the chars to remove
        (u' ' , u''),
        (u'　', u''),
        (u',' , u''),
        (u'，', u''),
        # unity the chars
        (u'台', u'臺'),
        (u'０', u'0'),
        (u'１', u'1'),
        (u'２', u'2'),
        (u'３', u'3'),
        (u'４', u'4'),
        (u'５', u'5'),
        (u'６', u'6'),
        (u'７', u'7'),
        (u'８', u'8'),
        (u'９', u'9'),
    )

    @staticmethod
    def normalize(s):
        if isinstance(s, str):
            s = s.decode('utf-8')
        for from_, to in Address.PAIRS_TO_NORMALIZE:
            s = s.replace(from_, to)
        return s

    @staticmethod
    def tokenize(addr_str):
        return tuple(Address.TOKEN_RE.findall(Address.normalize(addr_str)))

    def extract_no_pair(self, idx):
        try:
            token = self.tokens[idx]
        except IndexError:
            return (0, 0)
        else:
            return (
                int(token[Address.NO]    or 0),
                int(token[Address.SUBNO] or 0)
            )

    def __init__(self, addr_str):
        self.tokens = Address.tokenize(addr_str)

    @staticmethod
    def _flat(tokens, n):
        return u''.join(u''.join(token) for token in tokens[:n])

    def flat(self, n=None):
        return Address._flat(self.tokens, n)

    def __repr__(self):
        return 'Address(%r)' % self.flat()

class Rule(Address):

    RULE_TOKEN_RE = re.compile(u'''
        及以上附號|含附號以下|含附號全|含附號
        |
        以下|以上
        |
        附號全
        |
        [連至單雙全](?=[\d全]|$)
    ''', re.X)

    @staticmethod
    def extract_tokens(rule_str):

        rule_str = Address.normalize(rule_str)

        rule_tokens_list = []

        def extract_token(m):
            token = m.group()
            rule_tokens_list.append(token)
            if token == u'附號全':
                return u'號'
            return ''

        addr_str = Rule.RULE_TOKEN_RE.sub(extract_token, rule_str)

        return (tuple(rule_tokens_list), addr_str)

    def __init__(self, rule_str):
        self.rule_tokens, addr_str = Rule.extract_tokens(rule_str)
        Address.__init__(self, addr_str)

    def flat_rule_tokens(self, n=None):
        return Address._flat(self.rule_tokens, n)

    def __repr__(self):
        return 'Rule(%r)' % (self.flat()+self.flat_rule_tokens())

    def match(self, addr):

        # the part reserves for rule tokens
        my_last_idx = len(self.tokens)
        my_last_idx -= (bool(self.rule_tokens) and u'全' not in self.rule_tokens)
        my_last_idx -= (u'至' in self.rule_tokens)

        his_last_idx = len(addr.tokens)
        his_last_idx -= bool(self.rule_tokens)

        my_tokens_to_match = self.tokens[:my_last_idx]
        if my_tokens_to_match:

            # the addr's tokens whose unit bigger than rule's are ignorable
            start_unit = my_tokens_to_match[0][Address.UNIT]
            for his_start_idx, his_token in enumerate(addr.tokens):
                if his_token[Address.UNIT] == start_unit:
                    break

            his_tokens_to_match = addr.tokens[his_start_idx:his_last_idx]
            if len(my_tokens_to_match) != len(his_tokens_to_match):
                return False

            for my_token, his_token in zip(my_tokens_to_match, his_tokens_to_match):
                if my_token != his_token:
                    return False

        # check the rule tokens
        his_no_pair = addr.extract_no_pair(-1)
        my_no_pair = self.extract_no_pair(-1)
        for rule_token in self.rule_tokens:
            if (
                (rule_token == u'全'     and not his_no_pair != (0, 0)) or
                (rule_token == u'單'     and not his_no_pair[0] & 1 == 1) or
                (rule_token == u'雙'     and not his_no_pair[0] & 1 == 0) or
                (rule_token == u'至'     and not self.extract_no_pair(-2) <= his_no_pair <= my_no_pair) or
                (rule_token == u'附號全' and not his_no_pair[1] > 0) or
                (u'以上' in rule_token   and not his_no_pair >= my_no_pair) or
                (u'以下' in rule_token   and not his_no_pair <= my_no_pair)
            ):
                return False

        return True

from collections import defaultdict
import csv
from itertools import izip

class Directory(object):

    def __init__(self):
        self.tokens_zipcodes_map = defaultdict(set)
        self.zipcode_rule_strs_map = defaultdict(set)

    def load(self, zipcode, addr_str, rule_str):

        tokens = Address.tokenize(addr_str)
        for i in range(len(tokens), 0, -1):
            self.tokens_zipcodes_map[tokens[:i]].add(zipcode)

        self.zipcode_rule_strs_map[zipcode].add(addr_str+rule_str)

    def load_chp_csv(self, lines, skip_first=True):

        lines_iter = iter(lines)

        if skip_first:
            next(lines_iter)

        for row in csv.reader(lines_iter):
            self.load(row[0], ''.join(row[1:-1]), row[-1])

    def find_zipcodes(self, addr_str):

        addr = Address(addr_str)

        # if the addr is correct, it runs only once
        for i in range(len(addr.tokens), 0, -1):
            # 85% -> only one zipcode
            zipcodes = self.tokens_zipcodes_map.get(addr.tokens[:i])
            if zipcodes:
                break
        else:
            return set()

        # skip the matching check if the addr is not detail enough
        if addr.tokens[-1][Address.UNIT] not in u'巷弄號樓':
            return zipcodes

        # check the addr matches which zipcode
        for zipcode in zipcodes:
            # 60% -> 1~10 rule_str
            for rule_str in self.zipcode_rule_strs_map[zipcode]:
                if Rule(rule_str).match(addr):
                    return set([zipcode])

        return zipcodes

    def find(self, addr_str):

        zipcodes = self.find_zipcodes(addr_str)

        if len(zipcodes) == 1:
            return zipcodes.pop()

        # find the common part of the zipcodes
        zipcode_slices = []
        for col in izip(*zipcodes):
            if any(col[0] != c for c in col):
                break
            zipcode_slices.append(col[0])

        return ''.join(zipcode_slices)
