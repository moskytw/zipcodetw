#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import sys
from . import _chp_csv_path, _db_path
from .util import Directory


class CallbackIter(object):
    def __init__(self, iterable, callback):
        self.iterator = iter(iterable)
        self.callback = callback

    def __iter__(self):
        return self

    def next(self):
        next_item = next(self.iterator)
        self.callback()
        return next_item

def print_progress(current, maximum):
    # The progress bar is 80-character wide, containing:
    # A. 75 symbols of either "#" or whitespace.
    # B. An integer indicating percentage, whitespace-padded to 4 characters.
    # C. A percentage sign (%).
    BAR_WIDTH = 75
    progress = current / maximum
    hash_count = int(BAR_WIDTH * progress)
    line = ''.join([
        '#' * hash_count,
        ' ' * (BAR_WIDTH - hash_count),
        ('%d%%' % (100 * progress)).rjust(5),
    ])
    sys.stdout.write('\r')
    sys.stdout.write(line)
    sys.stdout.flush()

def hide_cursor():
    if os.name == 'posix':
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()

def show_cursor():
    if os.name == 'posix':
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

def build(chp_csv_path=None, db_path=None):

    # use default path if either path is not given.

    if chp_csv_path is None:
        chp_csv_path = _chp_csv_path
    if db_path is None:
        db_path = _db_path

    try:
        hide_cursor()

        # build the index
        dir_ = Directory(db_path)
        size = os.stat(chp_csv_path).st_size
        print_progress(0, size)
        with open(chp_csv_path) as csv_f:

            def progress_callback():
                print_progress(csv_f.tell(), size)

            iterable = CallbackIter(csv_f, progress_callback)
            dir_.load_chp_csv(iterable)
    finally:
        sys.stdout.write('\r')
        show_cursor()
        print

def build_cmd(chp_csv_path=None, db_path=None):
    '''Build a ZIP code index by the CSV from Chunghwa Post.

    -i, --chp-csv-path  The path of the CSV.
    -o, --db-path       The output path.
    '''

    print 'Building ZIP code index ...'
    build(chp_csv_path, db_path)
    print 'Done.'

if __name__ == '__main__':

    try:
        import clime
    except ImportError:
        build(*sys.argv[1:])
    else:
        clime.start(white_pattern=clime.CMD_SUFFIX)
