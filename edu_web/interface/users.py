# -*- coding:utf-8 -*-

import pymongo
import comm
import hashlib
from comm import get_default_img

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

def handle_rss(uid, cat_id_list):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    user_dict['rss_list'] = []
    for cat_id in cat_id_list:
        try:
            user_dict['rss_list'].append(int(cat_id))
        except:
            print 'illeagel cat_id:' + cat_id
    user_dict['rss_list'] = list(set(user_dict['rss_list']))
    del(user_dict['_id'])
    edu_db.user.update({'uid':uid}, {'$set':user_dict})
    return {'rescode':res_code_dict['success']}

def get_my_rss(uid):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    res = {}
    res['cat_list'] = []
    if not 'rss_list' in user_dict:
        res['recode'] = 1
        res['err'] = 'no rss booked'
        return res
    for cat_id in user_dict['rss_list']:
        cat_info = {}
        cat_dict = edu_db.cat.find_one({'cat_id':cat_id})
        cat_info['cat_id'] = cat_id
        cat_info['title'] = cat_dict['cat_name']
        cat_info['bg_image'] = get_default_img()
        cat_info['last_title'] = cat_dict['last_title']
        cat_info['last_modify'] = cat_dict['last_modify']
        res['cat_list'].append(cat_info)
    return res 

def get_rss_news_list(uid):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    temp_list = []
    if not 'rss_list' in user_dict:
        res = {}
        res['recode'] = 1
        res['err'] = 'no rss booked'
        return res
    for cat_id in user_dict['rss_list']:
        doc_list = edu_db.formal_news.find({'cat_id':cat_id})
        for doc in doc_list:
            temp_list.append(comm.transform_doc(doc))
    sorted(temp_list, key=lambda temp : temp['ts'])
    return temp_list

def get_rss_homepage(uid, page, page_max_cnt):
    res = {}
    res['doc_list'] = []
    temp_list = get_rss_news_list(uid)
    max_pos = min(len(temp_list), page*page_max_cnt)
    res['doc_list'] = temp_list[(page-1)*page_max_cnt : max_pos]
    if max_pos == len(temp_list):
        res['end'] = 1
    else:
        res['end'] = 0
    return res

def get_fav_news_list(uid, fav_id):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    temp_list = []
    if not 'fav_list' in user_dict:
        res = {}
        res['recode'] = 1
        res['err'] = 'no fav booked'
        return res
    if not fav_id in user_dict['fav_list']:
        res = {}
        res['rescode'] = 1
        res['err'] = 'fav_id is not existed in this user:' + str(uid)
        return res
    for doc_id in user_dict['fav_list'][fav_id]['doc_list']:
        doc = edu_db.formal_news.find_one({'doc_id':doc_id})
        temp_list.append(comm.transform_doc(doc))
    sorted(temp_list, key=lambda temp : temp['ts'])
    return temp_list

def get_fav_homepage(uid, fav_id, page, page_max_cnt):
    res = {}
    res['doc_list'] = []
    temp_list = get_fav_news_list(uid, fav_id)
    if type(temp_list) == dict():
        return temp_list
    max_pos = min(len(temp_list), page*page_max_cnt)
    res['doc_list'] = temp_list[(page-1)*page_max_cnt : max_pos]
    if max_pos == len(temp_list):
        res['end'] = 1
    else:
        res['end'] = 0
    return res

def get_my_fav(uid):
    edu_db = comm.create_conn()
    res = {}
    res['fav_list'] = []
    user_dict = edu_db.user.find_one({'uid':uid})
    if not 'fav_list' in user_dict:
        return res
    for fav_id, fav_info in user_dict['fav_list'].items():
        fav_dict = {}
        fav_dict['fav_id'] = fav_id
        fav_dict['uid'] = uid
        fav_dict['fav_name'] = fav_info['fav_name']
        fav_dict['doc_list'] = fav_info['doc_list']
        fav_dict['fav_icon'] = get_default_img()
        res['fav_list'].append(fav_dict)
    return res 

def handle_fav(uid, opt, fav_id, doc_id):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    if opt == opt_dict['add']:
        user_dict['fav_list'][fav_id]['doc_list'].append(doc_id)
    elif opt == opt_dict['remove']:
        user_dict['fav_list'][fav_id]['doc_list'].remove(doc_id)
    del(user_dict['_id'])
    edu_db.user.update({'uid':uid}, {'$set':user_dict}) 
    return {'rescode':res_code_dict['success']}

def handle_fav_set(uid, opt, fav_name, fav_id, doc_id):
    edu_db = comm.create_conn()
    user_dict = edu_db.user.find_one({'uid':uid})
    if not 'fav_list' in user_dict:
        user_dict['fav_list'] = {}
    if opt == opt_dict['add']:
        fav_id = hashlib.md5(fav_name).hexdigest()
        user_dict['fav_list'][fav_id] = {} 
        user_dict['fav_list'][fav_id]['fav_name'] = fav_name
        user_dict['fav_list'][fav_id]['doc_list'] = []
        if doc_id != '':
            user_dict['fav_list'][fav_id]['doc_list'].append(doc_id)
    if opt == opt_dict['remove']:
        del(user_dict['fav_list'][fav_id])
    del(user_dict['_id'])
    edu_db.user.update({'uid':uid}, {'$set':user_dict}) 
    return {'rescode':res_code_dict['success']}
    
