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

if __name__ == "__main__":
    # for test
    #print get_cat_guide()
    #print get_cat_homepage(10001, 1, 10)
    print get_news_homepage('4412B606B3CBBE349A61E94C76C45571')
