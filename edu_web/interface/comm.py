# -*- coding:utf-8 -*-

import pymongo

def create_conn():
    conn = pymongo.MongoClient()
    return conn['edu']
