# -*- coding: utf-8 -*-
import csv
from difflib import get_close_matches
from random import choice

with open('./Zip32_10301.csv') as files:
    csv_files = csv.reader(files)
    csv_files = [' '.join(i) for i in csv_files]
    print u'測試：', choice(csv_files)

#address = u'高雄市三民區大昌二路307-1號'
address = u'臺北市大安區金華街187號東樓204室'
print u'查詢：', address
print u'結果：'
for i in get_close_matches(address.encode('utf-8'), csv_files):
    print i
