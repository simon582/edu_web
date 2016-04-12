# -*- coding:utf-8 -*-

import pymongo

client = pymongo.MongoClient()
cat_table = client['edu']['cat']

with open('cats.csv') as cat_file:
    for line in cat_file.readlines():
        res = line.strip().split(',')
        prod = {}
        prod['father_id'] = int(res[0])
        prod['father_name'] = res[1]
        prod['cat_id'] = int(res[2])
        prod['cat_name'] = res[3]
        cat_table.save(prod)
