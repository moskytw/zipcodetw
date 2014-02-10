#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
from time import time
from os.path import join, splitext
from . import _package_root
from .util import Directory

def build_index_from_chp_csv(chp_csv_name):

    chp_csv_path = join(_package_root, chp_csv_name)
    db_path = splitext(chp_csv_path)[0]+'.db'

    csv_f = open(chp_csv_path)
    next(csv_f)

    dir_ = Directory(db_path)

    dir_.create_tables()
    for row in csv.reader(csv_f):
        dir_.put(
            ''.join(row[1:-1]).decode('utf-8'),
            row[-1].decode('utf-8'),
            row[0].decode('utf-8'),
        )

    dir_.commit()
    csv_f.close()

if __name__ == '__main__':

    try:
        import clime
        clime.start({'build': build_index_from_chp_csv})
    except ImportError:
        import sys
        build_index_from_chp_csv(*sys.argv[1:])
