#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Address(object):

    TOKEN_RE = re.compile(u'''
        (?:
            (?P<no>\d+)
            (?P<subno>之\d+)?
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

    TO_REPLACE_RE = re.compile(u'''
    [ 　,，台-]
    |
    [０-９]
    |
    [一二三四五六七八九]?
    十?
    [一二三四五六七八九]
    (?=[段路街巷弄號樓])
    ''', re.X)

    TO_REMOVE_SET = set(u' 　,，')

    TO_REPLACE_MAP = {
        u'-' : u'之', u'台': u'臺',
        u'一': u'1', u'二': u'2', u'三': u'3', u'四': u'4', u'五': u'5',
        u'六': u'6', u'七': u'7', u'八': u'8', u'九': u'9',
    }

    @staticmethod
    def normalize(s):

        if isinstance(s, str):
            s = s.decode('utf-8')

        def replace(m):

            found = m.group()

            if found in Address.TO_REMOVE_SET:
                return u''
            if found in Address.TO_REPLACE_MAP:
                return Address.TO_REPLACE_MAP[found]

            len_found = len(found)

            # 65296 = '０'; 65305 = '９'; 65248 = '０'-'0'
            if len_found == 1 and 65296 <= ord(found) <= 65305:
                return unichr(ord(found)-65248)

            # for '十一' to '九十九'
            if len_found == 2:
                return u'1'+Address.TO_REPLACE_MAP[found[1]]
            if len_found == 3:
                return Address.TO_REPLACE_MAP[found[0]]+Address.TO_REPLACE_MAP[found[2]]

        s = Address.TO_REPLACE_RE.sub(replace, s)

        return s

    @staticmethod
    def tokenize(addr_str):
        return tuple(Address.TOKEN_RE.findall(Address.normalize(addr_str)))

    def __init__(self, addr_str):
        self.tokens = Address.tokenize(addr_str)

    def __len__(self):
        return len(self.tokens)

    def flat(self, slice_arg=None, *other_slice_args):
        return u''.join(
            u''.join(token) for token in self.tokens[
                slice(slice_arg, *other_slice_args)
            ]
        )

    def __repr__(self):
        return 'Address(%r)' % self.flat()

    def parse(self, idx):
        try:
            token = self.tokens[idx]
        except IndexError:
            return (0, 0)
        else:
            return (
                int(token[Address.NO]        or 0),
                int(token[Address.SUBNO][1:] or 0)
            )

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
    def part(rule_str):

        rule_str = Address.normalize(rule_str)

        rule_tokens = set()

        def extract(m):

            token = m.group()
            retval = u''

            if token == u'連':
                token = u''
            elif token == u'附號全':
                retval = u'號'

            if token:
                rule_tokens.add(token)

            return retval

        addr_str = Rule.RULE_TOKEN_RE.sub(extract, rule_str)

        return (rule_tokens, addr_str)

    def __init__(self, rule_str):
        self.rule_tokens, addr_str = Rule.part(rule_str)
        Address.__init__(self, addr_str)

    def flat(self):
        return Address.flat(self)+u''.join(self.rule_tokens)

    def __repr__(self):
        return 'Rule(%r)' % self.flat()

    def match(self, addr):

        # the part reserves for rule tokens
        my_end_pos = len(self.tokens)
        my_end_pos -= bool(self.rule_tokens) and u'全' not in self.rule_tokens
        my_end_pos -= u'至' in self.rule_tokens

        his_end_pos = len(addr.tokens)
        his_end_pos -= bool(self.rule_tokens)

        my_tokens_to_match = self.tokens[:my_end_pos]
        if my_tokens_to_match:

            # the addr's tokens whose unit bigger than rule's are ignorable
            start_unit = my_tokens_to_match[0][Address.UNIT]
            his_start_pos = 0
            for his_token in addr.tokens:
                if his_token[Address.UNIT] != start_unit:
                    his_start_pos += 1
                else:
                    break

            his_tokens_to_match = addr.tokens[his_start_pos:his_end_pos]
            if len(my_tokens_to_match) != len(his_tokens_to_match):
                return False

            for my_token, his_token in zip(my_tokens_to_match, his_tokens_to_match):
                if my_token != his_token:
                    return False

        # check the rule tokens
        his_no_pair     = addr.parse(-1)
        my_no_pair      = self.parse(-1)
        my_asst_no_pair = self.parse(-2)
        for rt in self.rule_tokens:
            if (
                (rt == u'全'         and not his_no_pair > (0, 0)) or
                (rt == u'單'         and not his_no_pair[0] & 1 == 1) or
                (rt == u'雙'         and not his_no_pair[0] & 1 == 0) or
                (rt == u'以上'       and not his_no_pair >= my_no_pair) or
                (rt == u'以下'       and not his_no_pair <= my_no_pair) or
                (rt == u'至'         and not (
                    my_asst_no_pair <= his_no_pair <= my_no_pair or
                    u'含附號全' in self.rule_tokens and his_no_pair[0] == my_no_pair[0]
                )) or
                (rt == u'含附號'     and not  his_no_pair[0] == my_no_pair[0]) or
                (rt == u'附號全'     and not (his_no_pair[0] == my_no_pair[0] and his_no_pair[1] > 0)) or
                (rt == u'及以上附號' and not  his_no_pair >= my_no_pair) or
                (rt == u'含附號以下' and not (his_no_pair <= my_no_pair  or his_no_pair[0] == my_no_pair[0]))
            ):
                return False

        return True

import sqlite3
import csv
from functools import wraps

class Directory(object):

    @staticmethod
    def get_common_part(str_a, str_b):

        if str_a is None: return str_b
        if str_b is None: return str_a

        i = 0 # for the case range is empty
        for i in range(min(len(str_a), len(str_b))):
            if str_a[i] != str_b[i]:
                break
        else:
            i += 1

        return str_a[:i]

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def create_tables(self):

        self.cur.execute('''
            create table precise (
                addr_str text,
                rule_str text,
                zipcode  text,
                primary key (addr_str, rule_str)
            );
        ''')

        self.cur.execute('''
            create table gradual (
                addr_str text primary key,
                zipcode  text
            );
        ''')

    def put_precise(self, addr_str, rule_str, zipcode):

        self.cur.execute('insert or ignore into precise values (?, ?, ?);', (
            addr_str,
            rule_str,
            zipcode
        ))

        return self.cur.rowcount

    def put_gradual(self, addr_str, zipcode):

        self.cur.execute('''
            select zipcode
            from   gradual
            where  addr_str = ?;
        ''', (addr_str,))

        row = self.cur.fetchone()
        if row is None:
            stored_zipcode = None
        else:
            stored_zipcode = row[0]

        self.cur.execute('replace into gradual values (?, ?);', (
            addr_str,
            Directory.get_common_part(stored_zipcode, zipcode),
        ))

        return self.cur.rowcount

    def put(self, head_addr_str, tail_rule_str, zipcode):

        addr = Address(head_addr_str)

        # (a, b, c)
        self.put_precise(
            addr.flat(),
            head_addr_str+tail_rule_str,
            zipcode
        )

        # (a, b, c) -> (a,); (a, b); (a, b, c); (b,); (b, c); (c,)
        len_tokens = len(addr)
        for f in range(len_tokens):
            for l in range(f, len_tokens):
                for s in range(1, 2+(f == 0 and l == 2)):
                    self.put_gradual(
                        addr.flat(f, l+1, s),
                        zipcode
                    )

    def load_chp_csv(self, chp_csv_lines):

        self.create_tables()

        lines_iter = iter(chp_csv_lines)
        next(lines_iter)

        for row in csv.reader(lines_iter):
            self.put(
                ''.join(row[1:-1]).decode('utf-8'),
                row[-1].decode('utf-8'),
                row[0].decode('utf-8'),
            )

        self.commit()

    def get_rule_str_zipcode_pairs(self, addr_str):

        self.cur.execute('''
            select rule_str, zipcode
            from   precise
            where  addr_str = ?;
        ''', (addr_str,))

        return self.cur.fetchall()

    def get_gradual_zipcode(self, addr_str):

        self.cur.execute('''
            select zipcode
            from   gradual
            where  addr_str = ?;
        ''', (addr_str,))

        row = self.cur.fetchone()
        return row and row[0] or None

    def find(self, addr_str):

        addr = Address(addr_str)

        for i in range(len(addr.tokens), 0, -1):

            addr_str = addr.flat(i)

            rzpairs = self.get_rule_str_zipcode_pairs(addr_str)
            if rzpairs:
                for rule_str, zipcode in rzpairs:
                    if Rule(rule_str).match(addr):
                        return zipcode

            gzipcode = self.get_gradual_zipcode(addr_str)
            if gzipcode:
                return gzipcode

        return u''
