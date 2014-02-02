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
        (?P<unit>[縣市鄉鎮市區村里路街巷弄號樓])
    ''', re.X)

    NO = 0
    SUBNO = 1
    NAME = 2
    UNIT = 3

    @staticmethod
    def tokenize(addr_str):
        if isinstance(addr_str, str):
            addr_str = addr_str.decode('utf-8')
        addr_str = addr_str.replace(u' ', u'').replace(u'　', u'').replace(u',', u'').replace(u'，', u'')
        return tuple(Address.TOKEN_RE.findall(addr_str))

    @staticmethod
    def extract_no_pair(token):
        return (
            int(token[Address.NO]     or 0),
            int(token[Address.SUBNO] or 0)
        )

    def __init__(self, addr_str):

        self.addr_str = addr_str
        self.tokens = Address.tokenize(addr_str)
        self.first_no_token_idx = 0
        self.number_pair = (0, 0)

        len_tokens = len(self.tokens)
        while self.first_no_token_idx < len_tokens:
            if self.tokens[self.first_no_token_idx][Address.NO]:
                self.number_pair = Address.extract_no_pair(self.tokens[self.first_no_token_idx])
                break
            self.first_no_token_idx += 1

    def __repr__(self):
        return 'Address(%r)' % self.addr_str

    def __cmp__(self, other):

        for i in range(self.first_no_token_idx):
            if self.tokens[i] != other.tokens[i]:
                raise ValueError('incomparable addresses')

        return cmp(self.number_pair, other.number_pair)

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

        rule_tokens_list = []

        def extract_token(m):
            token = m.group()
            rule_tokens_list.append(token)
            if token == u'附號全':
                return u'號'
            return ''

        addr_str = AddressRule.RULE_TOKEN_RE.sub(extract_token, addr_rule_str)

        return (tuple(rule_tokens_list), addr_str)

    def __init__(self, addr_rule_str):

        self.addr_rule_str = addr_rule_str
        self.rule_tokens, addr_str = AddressRule.extract_tokens(addr_rule_str)
        Address.__init__(self, addr_str)

    def __repr__(self):
        return 'AddressRule(%r)' % self.addr_rule_str

    def match(self, addr):

        try:
            cmp_result = cmp(self, addr)
        except ValueError:
            return False

        if not self.rule_tokens:
            return cmp_result == 0

        for rule_token in self.rule_tokens:

            if rule_token == u'單' and not addr.number_pair[0] & 1 == 1:
                return False
            if rule_token == u'雙' and not addr.number_pair[0] & 1 == 0:
                return False
            if u'以上' in rule_token and not addr.number_pair >= self.number_pair:
                return False
            if u'以下' in rule_token and not addr.number_pair <= self.number_pair:
                return False
            if rule_token == u'至' and not self.number_pair <= addr.number_pair <= Address.extract_no_pair(self.tokens[self.first_no_token_idx+1]):
                return False

        return True
