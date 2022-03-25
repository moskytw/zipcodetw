#!/usr/bin/env python


import sys
import csv
import dbfread


DRY_RUN = True
DRY_RUN = False


table = dbfread.DBF('Zip33U/DBF/rall1.dbf', char_decode_errors='ignore')
writer = csv.writer(sys.stdout)

i = 0
writer.writerow(table.field_names)
for record in table:
    writer.writerow(list(record.values()))
    i += 1
    if DRY_RUN and i >= 10:
        sys.exit()
