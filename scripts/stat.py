#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from pprint import pprint

def print_report(target_dict):

    len_pairs = len(target_dict)
    print 'Pairs Number: {:>6,}'.format(len_pairs)
    print

    print 'Count Each Lengths of Values:'

    lenv_count_map = defaultdict(int)
    for k, v in target_dict.iteritems():
        lenv_count_map[len(v)] += 1
    total_count = sum(lenv_count_map.itervalues())

    for lenv, count in sorted(lenv_count_map.iteritems(), key=lambda k: k[1], reverse=True):
        print '{:>6,} | {:>6,} | {:>5.2f}%'.format(
            lenv,
            count,
            100.*count/total_count,
        )
    print

    print 'Total  : {:>6,}'.format(total_count)

if __name__ == '__main__':
    import zipcodetw
    print '# Tokens -> Zipcodes'
    print
    print_report(zipcodetw._dir.tokens_zipcodes_map)
    print
    print

    print '# Zipcode -> Rule Strs'
    print
    print_report(zipcodetw._dir.zipcode_rule_strs_map)
