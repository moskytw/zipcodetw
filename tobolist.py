# -*- coding: utf-8 -*-
import csv
from difflib import get_close_matches

with open('./Zip32_10301.csv') as files:
    csv_files = csv.reader(files)
    csv_files = [' '.join(i) for i in csv_files]
    #print csv_files[5]

address = u'高雄市三民區大昌二路'
print address
for i in get_close_matches(address.encode('utf-8'), csv_files):
    print i
