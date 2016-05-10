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

def get_last_news(cat_id):
    edu_db = pymongo.MongoClient()['edu']
    news_list = edu_db.formal_news.find({'cat_id':cat_id})
    last_title = ''
    last_modify = ''
    last_ts = 0
    for news in news_list:
        cur_ts = time.mktime(time.strptime(news['datetime'],'%Y-%m-%d'))
        if cur_ts > last_ts:
            last_ts = cur_ts
            last_title = news['title']
            last_modify = news['datetime']
    return last_title, last_modify

def refresh_last_in_cat():
    edu_db = pymongo.MongoClient()['edu']
    for prod in edu_db.cat.find():
        del(prod['_id'])
        prod['last_title'], prod['last_modify'] = get_last_news(prod['cat_id'])
        edu_db.cat.update({'cat_id':prod['cat_id']}, {'$set':prod})        

def refresh_last_in_cat():
    edu_db = pymongo.MongoClient()['edu']
    for prod in edu_db.cat.find():
        del(prod['_id'])
        prod['last_title'], prod['last_modify'] = get_last_news(prod['cat_id'])
        edu_db.cat.update({'cat_id':prod['cat_id']}, {'$set':prod})        

if __name__ == "__main__":
    refresh_last_in_cat()
    refresh_last_in_source()
    #work()
