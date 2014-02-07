#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.4'

from os.path import dirname, join
from .util import Directory

_project_root = dirname(__file__)

_dir = Directory(join(_project_root, '201311.db'))
find = _dir.find
