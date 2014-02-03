#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Address(object):

    TOKEN_RE = re.compile(u'''
        (?:
            (?P<no>\d+)
            (?:[之-](?P<subno>\d+))?
            |
            (?P<name>.+?)
        )
        (?:
            [,，]
            |
            (?P<unit>[縣市鄉鎮市區村里路段街巷弄號樓])[,，]?
        )
    ''', re.X)

    NO    = 0
    SUBNO = 1
    NAME  = 2
    UNIT  = 3

    @staticmethod
    def normalize(s):
        if isinstance(s, str):
            s = s.decode('utf-8')
        return s.replace(u' ', u'').replace(u'　', u'')

    @staticmethod
    def tokenize(addr_str):
        return tuple(Address.TOKEN_RE.findall(Address.normalize(addr_str)))

    @staticmethod
    def flat(tokens, n=None):
        return tuple(u''.join(token) for token in tokens[:n])

    def extract_no_pair(self, idx):
        try:
            return (
                int(self.tokens[idx][Address.NO]    or 0),
                int(self.tokens[idx][Address.SUBNO] or 0)
            )
        except IndexError:
            return (0, 0)

    def __init__(self, addr_str=None, tokens=None, last_no_pair=None):

        if addr_str is  None:
            assert not (tokens is None or last_no_pair is None)
            self.tokens = tokens
            self.last_no_pair = last_no_pair
            return

        self.tokens = Address.tokenize(addr_str)
        self.last_no_pair = self.extract_no_pair(-1)

    def __repr__(self):
        return 'Address(tokens=%r, last_no_pair=%r)' % (
            self.tokens,
            self.last_no_pair
        )

class Rule(Address):

    RULE_TOKEN_RE = re.compile(u'''
        及以上附號|含附號以下|含附號全|含附號
        |
        以下|以上
        |
        附號全
        |
        [連至](?=\d)
        |
        [單雙](?=[\d全])
        |
        全(?=$)
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

    def __init__(self, rule_str=None, tokens=None, last_no_pair=None, rule_tokens=None):

        if rule_str is None:
            assert not rule_tokens is None
            self.rule_tokens = rule_tokens
            Address.__init__(self, tokens=tokens, last_no_pair=last_no_pair)
            return

        self.rule_tokens, addr_str = Rule.extract_tokens(rule_str)
        Address.__init__(self, addr_str)

    def __repr__(self):
        return 'Rule(tokens=%r, last_no_pair=%r, rule_tokens=%r)' % (
            self.tokens,
            self.last_no_pair,
            self.rule_tokens
        )

    def match(self, addr):

        my_tokens_to_match = self.tokens[:-(self.last_no_pair != (0, 0))-(u'至' in self.rule_tokens) or None]
        if my_tokens_to_match:

            if len(addr.tokens) < len(my_tokens_to_match):
                return False

            start_unit = my_tokens_to_match[0][Address.UNIT]
            for i, his_token in enumerate(addr.tokens):
                if his_token[Address.UNIT] == start_unit:
                    break

            for my_token, his_token in zip(my_tokens_to_match, addr.tokens[i:]):
                if my_token != his_token:
                    return False

            if not self.rule_tokens:
                return addr.last_no_pair == self.last_no_pair

        his_no_pair = addr.last_no_pair
        my_no_pair = self.last_no_pair
        for rule_token in self.rule_tokens:
            if (
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
        self.tokens_zipcodes_map = defaultdict(list)
        self.zipcode_rule_strs_map = defaultdict(list)

    def load(self, zipcode, addr_str, rule_str):

        tokens = Address.tokenize(addr_str)
        for i in range(len(tokens), 0, -1):
            self.tokens_zipcodes_map[tokens[:i]].append(zipcode)

        self.zipcode_rule_strs_map[zipcode].append(addr_str+rule_str)

    def load_chp_csv(self, lines, skip_first=True):

        lines_iter = iter(lines)

        if skip_first:
            next(lines_iter)

        for row in csv.reader(lines_iter):
            self.load(row[0], ''.join(row[1:-1]), row[-1])

    def find(self, addr_str):

        addr = Address(addr_str)

        for i in range(len(addr.tokens), 0, -1):
            zipcodes = self.tokens_zipcodes_map.get(addr.tokens[:i])
            if zipcodes is not None:
                break
        else:
            return []

        if addr.last_no_pair == (0, 0):
            return zipcodes

        for zipcode in zipcodes:
            for rule_str in self.zipcode_rule_strs_map[zipcode]:
                if Rule(rule_str).match(addr):
                    return [zipcode]

        return zipcodes

    def fuzzy_find(self, addr_str):

        zipcodes = self.find(addr_str)

        if len(zipcodes) == 1:
            return zipcodes[0]

        zipcode_slices = []
        for col in izip(*zipcodes):
            if any(col[0] != c for c in col):
                break
            zipcode_slices.append(col[0])

        return ''.join(zipcode_slices)
