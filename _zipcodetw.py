#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'

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
            (?P<unit>[縣市鄉鎮市區村里路段街巷弄號樓])
            |
            (?=\d|$)
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

    @staticmethod
    def flat(tokens, n=None):
        return tuple(u''.join(token) for token in tokens[:n])

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

        last_must_match_idx = len(self.tokens)
        last_must_match_idx -= (bool(self.rule_tokens) and u'全' not in self.rule_tokens)
        last_must_match_idx -= (u'至' in self.rule_tokens)

        my_tokens_must_match = self.tokens[:last_must_match_idx]
        if my_tokens_must_match:

            if len(addr.tokens) < len(my_tokens_must_match):
                return False

            start_unit = my_tokens_must_match[0][Address.UNIT]
            for i, his_token in enumerate(addr.tokens):
                if his_token[Address.UNIT] == start_unit:
                    break

            for my_token, his_token in zip(my_tokens_must_match, addr.tokens[i:]):
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

        # multiple rows may map to a same zip code
        self.zipcode_rule_strs_map[zipcode].append(addr_str+rule_str)

    def load_chp_csv(self, lines, skip_first=True):

        lines_iter = iter(lines)

        if skip_first:
            next(lines_iter)

        for row in csv.reader(lines_iter):
            self.load(row[0], ','.join(row[1:-1]), row[-1])

    def find_zipcodes(self, addr_str):

        addr = Address(addr_str)

        for i in range(len(addr.tokens), 0, -1):
            zipcodes = self.tokens_zipcodes_map.get(addr.tokens[:i])
            if zipcodes:
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

    def find(self, addr_str):

        zipcodes = self.find_zipcodes(addr_str)

        if len(zipcodes) == 1:
            return zipcodes[0]

        zipcode_slices = []
        for col in izip(*zipcodes):
            if any(col[0] != c for c in col):
                break
            zipcode_slices.append(col[0])

        return ''.join(zipcode_slices)
