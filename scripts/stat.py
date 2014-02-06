#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from pprint import pprint

def print_report(target_dict, key=None):

    len_pairs = len(target_dict)
    print 'Length of This Dict: {:>6,}'.format(len_pairs)
    print

    lenio_count_map = defaultdict(int)
    for k, v in target_dict.iteritems():
        lenio_count_map[(len(k), len(v))] += 1
    total_count = sum(lenio_count_map.itervalues())

    print 'Count of Each Length of Input, Output Pair:'
    print

    cum_pct = .0
    for lenio, count in sorted(lenio_count_map.iteritems(), key=key):
        pct = 100.*count/total_count
        cum_pct += pct
        print ' {:7} | {:>7,} | {:>6.2f}% | {:>6.2f}%'.format(lenio, count, pct, cum_pct)
    print

    print 'Total  : {:>6,}'.format(total_count)
    print 'Average: {:>9,.2f}'.format(1.*total_count/len(lenio_count_map))

if __name__ == '__main__':

    from time import time

    start = time()
    import zipcodetw
    end = time()

    print 'Took {:.2f}s to load.'.format(end-start)
    print

    print '# Tokens -> Rule Str, Zipcode Pairs (smaller is better)'
    print
    print_report(zipcodetw._dir.tokens_rzpairs_map)
    print
    print

    print '# Tokens -> Gradual Zipcode (bigger is better)'
    print
    print_report(zipcodetw._dir.tokens_gzipcode_map, key=lambda p: (p[0][0], -p[0][1]))
