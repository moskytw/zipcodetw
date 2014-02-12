#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from . import _chp_csv_path, _db_path
from .util import Directory

def build(chp_csv_path=None, db_path=None):

    # use default path if either path is not given.

    if chp_csv_path is None:
        chp_csv_path = _chp_csv_path
    if db_path is None:
        db_path = _db_path

    # build the index

    dir_ = Directory(db_path)
    with open(chp_csv_path) as csv_f:
        dir_.load_chp_csv(csv_f)

def build_cmd(chp_csv_path=None, db_path=None):
    '''Build a ZIP code index by the CSV from Chunghwa Post.

    -i, --chp-csv-path  The path of the CSV.
    -o, --db-path       The output path.
    '''

    print 'Building ZIP code index ...',
    sys.stdout.flush()
    build(chp_csv_path, db_path)
    print 'Done.'

if __name__ == '__main__':

    try:
        import clime
    except ImportError:
        build(*sys.argv[1:])
    else:
        clime.start(white_pattern=clime.CMD_SUFFIX)
