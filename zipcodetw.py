#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

with open('zipcodetw-20140131.csv') as f:
    for row in csv.reader(f):
        zipcode = row[0]
        address_tuple = row[1:-1]
        rule_str = row[-1]
        print zipcode, address_tuple, rule_str
