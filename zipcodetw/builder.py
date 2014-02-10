#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from os.path import splitext
from .util import Directory

def build_index_from_chp_csv(chp_csv_path):

    db_path = splitext(chp_csv_path)[0]+'.db'

    dir_ = Directory(db_path)
    dir_.create_tables()

    csv_f = open(chp_csv_path)
    next(csv_f)
    for row in csv.reader(csv_f):
        dir_.put(
            ''.join(row[1:-1]).decode('utf-8'),
            row[-1].decode('utf-8'),
            row[0].decode('utf-8'),
        )
    csv_f.close()

    dir_.commit()

if __name__ == '__main__':

    try:
        import clime
        clime.start({'build': build_index_from_chp_csv})
    except ImportError:
        import sys
        build_index_from_chp_csv(*sys.argv[1:])
