#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.6'

from os.path import dirname, join
from .util import Directory

# paths
_package_root = dirname(__file__)
_chp_csv_path = join(_package_root, '201412.csv')
_db_path = join(_package_root, '201412.db')

# make a directory
_dir = Directory(_db_path)

# the API only exposed
find = _dir.find
