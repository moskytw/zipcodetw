#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from pprint import pprint

def print_report(target_dict):

    len_pairs = len(target_dict)
    print 'Pairs Number: {:>6,}'.format(len_pairs)
    print

    print 'Count Length of Each Key and Value Pair:'

    lenkv_count_map = defaultdict(int)
    for k, v in target_dict.iteritems():
        lenkv_count_map[(len(k), len(v))] += 1
    total_count = sum(lenkv_count_map.itervalues())

    cum_pct = .0
    for lenkv, count in sorted(lenkv_count_map.iteritems(), key=lambda k: k[0]):
        pct = 100.*count/total_count
        cum_pct += pct
        print ' {:7} | {:>7,} | {:>6.2f}% | {:>6.2f}%'.format(lenkv, count, pct, cum_pct)
    print

    print 'Total  : {:>6,}'.format(total_count)
    print 'Average: {:>9,.2f}'.format(1.*total_count/len(lenkv_count_map))

if __name__ == '__main__':

    from time import time

    start = time()
    import zipcodetw
    end = time()

    print '# Tokens -> Rule Str and Zipcode Pairs'
    print
    print_report(zipcodetw._dir.tokens_rzpairs_map)
    print
    print

    print '# Tokens -> Gradual Zipcode'
    print
    print_report(zipcodetw._dir.tokens_gzipcode_map)
    print
    print

    print 'Took {:.2f}s to load.'.format(end-start)
