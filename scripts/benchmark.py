#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from timeit import timeit

start = time()
import zipcodetw
end = time()

print 'The package took {:.2f} seconds to load.'.format(end-start)

def test_find():

    zipcodetw.find('台北市')
    zipcodetw.find('台北市中正區')
    zipcodetw.find('台北市中正區仁愛路')
    zipcodetw.find('台北市中正區仁愛路2段')
    zipcodetw.find('台北市中正區仁愛路2段45號')

    zipcodetw.find('台中市')
    zipcodetw.find('台中市中區')
    zipcodetw.find('台中市中區台灣大道')
    zipcodetw.find('台中市中區台灣大道1段')
    zipcodetw.find('台中市中區台灣大道1段239號')

    zipcodetw.find('臺南市')
    zipcodetw.find('臺南市中西區')
    zipcodetw.find('臺南市中西區府前路')
    zipcodetw.find('臺南市中西區府前路1段')
    zipcodetw.find('臺南市中西區府前路1段226號')

n = 1000
print 'Timeit test_find with n={} took {:.2f} seconds.'.format(n, timeit(test_find, number=n))
