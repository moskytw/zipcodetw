#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, join
from _zipcodetw import Directory, __version__

_project_root = dirname(__file__)

_dir = Directory(join(_project_root, '201311.db'))
find = _dir.find
