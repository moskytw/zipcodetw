The ZIP Code Finder for Taiwan
==============================

It converts address to ZIP code quickly.

The main features:

1. Fast. It uses tokenization to build the ZIP code index.
2. Gradual. It allows a partial address to match partial ZIP code.
3. Lightweight. It depends on nothing.

Usage
-----

>>> import zipcodetw

>>> zipcodetw.find('臺北市')
'1'
>>> zipcodetw.find('臺北市信義區')
'110'
>>> zipcodetw.find('臺北市信義區市府路')
'110'
>>> zipcodetw.find('臺北市信義區市府路1號')
'11008'

>>> zipcodetw.find_zipcodes('臺北市信義區市府路')
['11060', '11008', '11073', '11001', '11073']

Have fun. :)

Data
----

The ZIP code data are provided by Chunghwa Post. The CSV are available here: http://www.post.gov.tw/post/internet/down/index.html#1808
