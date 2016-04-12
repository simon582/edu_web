# -*- coding:utf-8 -*-

import pymongo
import datetime
import time

def work():
    edu_db = pymongo.MongoClient()['edu']
    for prod in edu_db.news.find():
        if edu_db.formal_news.count({"doc_id":prod['doc_id']}) > 0:
            continue
        del(prod['_id'])
        del(prod['createtime'])
        prod['share_cnt'] = 0
        prod['collection_cnt'] = 0
        prod['like_cnt'] = 0
        prod['ts'] = time.mktime(time.strptime(prod['datetime'],'%Y-%m-%d')) 
        edu_db.formal_news.save(prod)
        print 'transform ' + prod['doc_id']       

if __name__ == "__main__":
    work()
