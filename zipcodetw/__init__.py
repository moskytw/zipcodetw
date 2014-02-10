#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.5'

from os.path import getsize, dirname, join
from .util import Directory

_package_root = dirname(__file__)
_chp_csv_path = join(_package_root, '201311.csv')
_db_path = join(_package_root, '201311.db')

if getsize(_db_path) == 0:
    import sys
    print >> sys.stderr, 'Warning: The size of ZIP code index is zero.'
    print >> sys.stderr, '         Use python -m zipcodetw.builder to build.'

_dir = Directory(_db_path)
find = _dir.find
