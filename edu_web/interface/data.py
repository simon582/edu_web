# -*- coding:utf-8 -*-

import comm
import os
import random

def get_default_img():
    default_img_dir = '/data/edu/default_img/'
    img_list = os.listdir(default_img_dir)
    return '/media/default_img/' + random.choice(img_list)        

def get_cat_guide():
    cat_list = []
    edu_db = comm.create_conn()
    father_cat_list = edu_db.cat.distinct("father_id")
    for fcat_id in father_cat_list:
        cat = {}
        cat['cat_id'] = fcat_id
        cat['sub_cat'] = []
        for prod in edu_db.cat.find({'father_id':fcat_id}):
            if not 'title' in prod:
                prod['title'] = prod['father_name']
            sub_cat = {}
            sub_cat['cat_id'] = prod['cat_id']
            sub_cat['title'] = prod['cat_name']
            sub_cat['bg_image'] = get_default_img()
            cat['sub_cat'].append(sub_cat)
        cat_list.append(cat) 
    return cat_list

def transform_doc(doc):
    del(doc['_id'])
    text = ''
    for t in doc['text']:
        text += t + '<br>'
        if len(text) > 100:
            break
    doc['text'] = text
    if not 'bg_image' in doc:
        doc['bg_image'] = get_default_img()
    return doc 

def get_cat_homepage(cat_id, page, page_max_cnt):
    edu_db = comm.create_conn()
    prod = {}
    prod['doc_list'] = []
    doc_list = edu_db.formal_news.find({'cat_id':cat_id})
    temp_list = []
    for doc in doc_list:
        temp_list.append(transform_doc(doc))
    sorted(temp_list, key=lambda temp : temp['ts'])
    max_pos = min(len(temp_list)-1, (page+1)*page_max_cnt) 
    prod['doc_list'] = temp_list[page*page_max_cnt : max_pos]
    if max_pos == len(temp_list)-1:
        prod['end'] = 1
    else:
        prod['end'] = 0
    return prod

def get_news_homepage(doc_id):
    edu_db = comm.create_conn()
    prod = {}
    doc = edu_db.formal_news.find_one({"doc_id":doc_id})
    prod['text'] = ''
    for t in doc['text']:
        prod['text'] == t + '<br>'
    prod['base'] = transform_doc(doc)
    return prod

def get_query(query, page, page_max_cnt):
    edu_db = comm.create_conn()
    res = {}
    res['doc_list'] = []
    temp_list = []
    for prod in edu_db.formal_news.find():
        if prod['title'].find(query) != -1:
            temp_list.append(transform_doc(doc))
    sorted(temp_list, key=lambda temp : temp['ts'])
    max_pos = min(len(temp_list)-1, (page+1)*page_max_cnt) 
    res['doc_list'] = temp_list[page*page_max_cnt : max_pos]
    if max_pos == len(temp_list)-1:
        res['end'] = 1
    else:
        res['end'] = 0
    return res

def get_source():
    #edu_db = comm.create_conn()
    #source_list = edu_db.news.distinct("source")
    res = {}
    res['source_list'] = []
    source_info = {}
    source_info['source'] = 'eol'
    source_info['source_desc'] = '中国教育在线'
    source_info['bg_image'] = get_default_img()
    source_info['last_title'] = ''
    source_info['last_modify'] = ''
    res['source_list'].append(source_info)
    return res

def get_source_homepage(source_name, page, page_max_cnt):
    edu_db = comm.create_conn()
    prod = {}
    prod['doc_list'] = []
    doc_list = edu_db.formal_news.find({'source_name':source_name})
    temp_list = []
    for doc in doc_list:
        temp_list.append(transform_doc(doc))
    sorted(temp_list, key=lambda temp : temp['ts'])
    max_pos = min(len(temp_list)-1, (page+1)*page_max_cnt) 
    prod['doc_list'] = temp_list[page*page_max_cnt : max_pos]
    if max_pos == len(temp_list)-1:
        prod['end'] = 1
    else:
        prod['end'] = 0
    return prod

def handle_share(doc_id):
    edu_db = comm.create_conn()
    prod = edu_db.formal_news.find_one({'doc_id':doc_id})
    del(prod['_id'])
    prod['share_cnt'] += 1
    edu_db.formal_news.update({'doc_id':doc_id}, {'$set':prod})
    return {'rescode':0}

# TODO
def handle_like(doc_id):
    edu_db = comm.create_conn()
    prod = edu_db.formal_news.find_one({'doc_id':doc_id})
    del(prod['_id'])
    prod['like_cnt'] += 1
    edu_db.formal_news.update({'doc_id':doc_id}, {'$set':prod})
    return {'rescode':0}


if __name__ == "__main__":
    # for test
    #print get_cat_guide()
    #print get_cat_homepage(10001, 1, 10)
    print get_news_homepage('4412B606B3CBBE349A61E94C76C45571')
