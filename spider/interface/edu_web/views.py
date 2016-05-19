# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.http import HttpResponse
import json
import pymongo
import hashlib

def get_int_val(key_name, request):
    try:
        val = int(request.POST.get(key_name, -1))
        if val == -1:
            return False, 'no ' + key_name
    except:
        return False, 'invalid ' + key_name
    return True, val

def get_str_val(key_name, request):
    try:
        val = request.POST.get(key_name, -1)
        if val == -1:
            return False, 'no ' + key_name
    except:
        return False, 'invalid ' + key_name
    return True, val

def get_list_val(key_name, request):
    try:
        val = request.POST.get(key_name, -1)
        if val == -1:
            return False, 'no ' + key_name
        val_list = val.split(',')
    except:
        return False, 'invalid ' + key_name
    return True, val_list

def write_news(news):
    edu_db = pymongo.MongoClient()['edu']
    news['doc_id'] = hashlib.md5(news['title']).hexdigest().upper()
    try:
        edu_db.temp.save(news)
    except Exception as e:
        print e
        print 'doc_id:%s has existed' % news['doc_id']

def handle_request(request):
    prod = {}
    prod['rescode'] = 0
    prod['msg'] = 'success'
    
    news = {}
    key_list = [
        'title',
        'source',
        'detail_url',
        'create_time',
        'author',
        'publish_time',
        'title',
        'text',
    ]

    stat = True
    for key in key_list:
        stat, news[key] = get_str_val(key, request)
        if not stat:
            prod['rescode'] = 1
            prod['msg'] = news[key]
            break
   
    if stat:
        write_news(news)    
 
    return HttpResponse(json.dumps(prod, ensure_ascii=False))
