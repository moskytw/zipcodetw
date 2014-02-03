The ZIP Code Finder for Taiwan
==============================

It let you find ZIP code by fuzzy address.

>>> import zipcodetw
>>> zipcodetw.find('臺北市')
'1'
>>> zipcodetw.find('臺北市信義區')
'110'
>>> zipcodetw.find('臺北市信義區市府路')
'110'
>>> zipcodetw.find('臺北市信義區市府路1號')
'11008'
