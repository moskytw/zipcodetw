#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, join
from _zipcodetw import Directory, __version__

_ROOT = dirname(__file__)

_dir = Directory()
_dir.load_chp_csv(open(join(_ROOT, '201311.csv')))

find_zipcodes = _dir.find_zipcodes
find = _dir.find
