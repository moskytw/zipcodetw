#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from os.path import splitext
from .util import Directory

def build(chp_csv_path):

    db_path = splitext(chp_csv_path)[0]+'.db'

    dir_ = Directory(db_path)

    with open(chp_csv_path) as csv_f:
        dir_.load_chp_csv(csv_f)

if __name__ == '__main__':

    try:
        import clime
        clime.start({'build': build})
    except ImportError:
        import sys
        build(*sys.argv[1:])
