#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.5.6'

from os.path import dirname, join
from .util import Directory
from .util import AddressEnglishTranslator

# paths
_package_root = dirname(__file__)
_chp_csv_path = join(_package_root, '201311.csv')
_db_path = join(_package_root, '201311.db')
_county_path = join(_package_root, 'county_h_2013-12-16.csv')
_village_path = join(_package_root, 'Village_H_10208.txt')
_rd_st_path = join(_package_root, 'CE_Rd_St_H_12011.csv')

# make a directory
_dir = Directory(_db_path)
_translator = AddressEnglishTranslator(_county_path, _village_path, _rd_st_path)

# the API only exposed
find = _dir.find
translate = _translator.translate