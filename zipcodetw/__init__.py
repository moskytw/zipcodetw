#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'

from os.path import join, normpath
from zipcodetw.util import Directory

_package_dir = normpath(join(__file__, '..'))

_dir = Directory()
_dir.load_chp_csv(open(join(_package_dir, 'zipcodetw-201311.csv')))

find_zipcodes = _dir.find_zipcodes
find = _dir.find
