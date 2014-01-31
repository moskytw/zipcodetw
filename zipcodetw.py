#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uniout
import csv
import re

rule_re = re.compile(u'''
    (?P<lane>       \d+巷)?
    (?P<alley>      \d+弄)?
    (?P<greater>    [單雙連]?\d+(?:之\d+)?[巷弄號](?:含附號)?以上(?:附號)?)?
    (?P<lesser>     [單雙連]?\d+(?:之\d+)?[巷弄號](?:含附號)?以下(?:附號)?)?
    (?P<range>      [單雙連]?\d+(?:之\d+)?[巷弄號]?至(?:\d+)?(?:之\d+)?[巷弄號](?:含附號全)?)?
    (?P<number>     [單雙連]?\d+(?:之\d+)?[巷弄號]?(?:含附號|附號全|及以上附號)?)?
    (?P<all>        [單雙連]?全)?
    (?P<comment>     \(.+\)?)?
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
            #print rule_m.groupdict()
            counter += 1

    print counter
