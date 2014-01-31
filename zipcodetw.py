#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uniout
import csv
import re

# The regex:
#
# * <odd_or_even>: 60749
# * + <all>      : 23376
# * + <lane>     : 22383
# * + <alley>    : 22319
# * + <number>   : 21318
#

rule_re = re.compile(u'''
    (?P<odd_or_even>[單雙])?
    (?P<lane>       \d+巷 )?
    (?P<alley>      \d+弄 )?
    (?P<number>     \d+(之\d+)?號)?
    (?P<range>      \d+(之\d+)?號至\d+(之\d+)?號)?
    (?P<all>        全    )?
    (?P<skipped>   .+     )?
''', re.X)

with open('zipcodetw-20140131.csv') as f:

    next(f)

    counter = 0

    for row in csv.reader(f):

        zipcode = row[0]
        address_tuple = row[1:-1]
        rule_str = row[-1].decode('utf-8').replace(u' ', u'').replace(u'　', u'')

        #print zipcode, address_tuple, rule_str

        rule_m = rule_re.match(rule_str)
        if rule_m.group('skipped'):
            print rule_str
            print rule_m.groupdict()
            counter += 1

    print counter
