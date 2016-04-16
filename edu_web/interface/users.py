# -*- coding:utf-8 -*-

import pymongo
import comm
import hashlib

res_code_list = [
    'success',
    'wrong_username_or_password',
    'user_is_exist',
]

res_code_dict = comm.generate_enum_dict(res_code_list)

def current_max_uid(edu_db):
    max_uid = 10000
    for prod in edu_db.user.find():
        if prod['uid'] > max_uid:
            max_uid = prod['uid']
    return max_uid

def register_user(username, passwd, category, data):
    edu_db = comm.create_conn()
    cnt = edu_db.user.count({"username":username})
    if cnt > 0:
        return {'rescode':res_code_dict['user_is_exist']}
    prod = {}
    prod['username'] = username
    prod['passwd'] = passwd
    prod['category'] = category
    prod['uid'] = current_max_uid(edu_db) + 1
    prod['data'] = data
    edu_db.user.save(prod)
    res = {}
    res['rescode'] = res_code_dict['success']
    res['uid'] = prod['uid']
    res['username'] = prod['username']
    res['others'] = ''
    return res

def login_user(username, passwd):
    edu_db = comm.create_conn()
    prod = edu_db.user.find_one({"username":username, "passwd":passwd})
    res = {}
    if not prod:
        res['rescode'] = res_code_dict['wrong_username_or_password']
    else:
        res['rescode'] = res_code_dict['success']
        res['uid'] = prod['uid']
        res['username'] = prod['username']
        res['other'] = ''
    return res

opt_list = [
    'add',
    'remove',
]
opt_dict = comm.generate_enum_dict(opt_list)

def handle_rss(uid, cat_id_list, opt):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    if opt == opt_dict['add']:
        if not 'rss_list' in user_dict:
            user_dict['rss_list'] = []
        for cat_id in cat_id_list:
            user_dict['rss_list'].append(cat_id)
        user_dict['rss_list'] = list(set(user_dict['rss_list']))
    if opt == opt_dict['remove']:
        for cat_id in cat_id_list:
            user_dict['rss_list'].remove(cat_id)
    del(user_dict['_id'])
    edu_db.user.update({'uid':uid}, {'$set':user_dict})
    return {'rescode':res_code_dict['success']}
