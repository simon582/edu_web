# -*- coding:utf-8 -*-

import pymongo

def generate_enum_dict(type_list):
    type_dict = {}
    for tid in xrange(len(type_list)):
        type_dict[type_list[tid]] = tid
    return type_dict

def create_conn():
    conn = pymongo.MongoClient()
    return conn['edu']
