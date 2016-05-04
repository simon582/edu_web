# -*- coding:utf-8 -*-

import pymongo
import random
import os

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

def get_default_img():
    default_img_dir = '/data/edu/default_img/'
    img_list = os.listdir(default_img_dir)
    return 'http://121.196.226.177:8080/media/default_img/' + random.choice(img_list)

def generate_enum_dict(type_list):
    type_dict = {}
    for tid in xrange(len(type_list)):
        type_dict[type_list[tid]] = tid
    return type_dict

def create_conn():
    conn = pymongo.MongoClient()
    return conn['edu']
