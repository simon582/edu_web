# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import mock_data
from django.http import HttpResponse
import json
sys.path.append('./edu_web/interface')
import users
import news

def get_int_val(key_name, request):
    try:
        val = int(request.GET.get(key_name, -1))
        if val == -1:
            return False, 'no ' + key_name
    except:
        return False, 'invalid ' + key_name
    return True, val

def get_str_val(key_name, request):
    try:
        val = request.GET.get(key_name, -1)
        if val == -1:
            return False, 'no ' + key_name
    except:
        return False, 'invalid ' + key_name
    return True, val

def get_list_val(key_name, request):
    try:
        val = request.GET.get(key_name, -1)
        if val == -1:
            return False, 'no ' + key_name
        val_list = val.split(',')
    except:
        return False, 'invalid ' + key_name
    return True, val_list

def normal_work(tid, qid, request):
    global news
    prod = {}
    prod['rescode'] = 0
    stat, prod['qid'] = get_str_val('qid', request)
    if not stat:
        prod['rescode'] = 1
        prod['err'] = prod['qid']

    # 欢迎
    if tid == mock_data.type_dict['welcome']:
        prod['img_url'] = ''

    # 获取分类
    elif tid == mock_data.type_dict['cat_guide']:
        prod['cat_list'] = news.get_cat_guide()

    # 登录
    elif tid == mock_data.type_dict['login']:
        stat1, username = get_str_val('username', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = username
        stat2, passwd = get_str_val('passwd', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = passwd
        if stat1 and stat2:
            res = users.login_user(username, passwd)
            for k,v in res.items():
                prod[k] = v
 
    # 注册
    elif tid == mock_data.type_dict['register']:
        stat1, username = get_str_val('username', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = username
        stat2, passwd = get_str_val('passwd', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = passwd
        stat3, category = get_int_val('category', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = category
        stat4, data = get_str_val('data', request)
        if not stat4:
            prod['rescode'] = 1
            prod['err'] = data
        
        if stat1 and stat2 and stat3 and stat4:
            res = users.register_user(username, passwd, category, news)
            for k,v in res.items():
                prod[k] = v

    # 分类主页
    elif tid == mock_data.type_dict['cat_homepage']:
        stat1, cat_id = get_int_val('cat_id', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = cat_id
        stat2, page = get_int_val('page', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = page
        stat3, page_max_cnt = get_int_val('page_max_cnt', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = page_max_cnt
        if stat1 and stat2 and stat3:
            res = news.get_cat_homepage(cat_id, page, page_max_cnt)
            for k,v in res.items():
                prod[k] = v

    # 新闻主页
    elif tid == mock_data.type_dict['news_homepage']:
        stat1, doc_id = get_str_val('doc_id', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = doc_id
        stat2, list_type = get_str_val('list_type', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = list_type
        stat3, list_desc = get_str_val('list_desc', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = list_desc
        if stat1 and stat2 and stat3:
            res = news.get_news_homepage(doc_id, list_type, list_desc)
            for k,v in res.items():
                prod[k] = v

    # 个人主页        
    elif tid == mock_data.type_dict['my_homepage']:
        prod['portrait_url'] = ''
        prod['others'] = ''

    # 增删订阅分类
    elif tid == mock_data.type_dict['handle_rss']:
        stat1, uid = get_int_val('uid', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = uid
        stat2, opt = get_int_val('opt', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = opt
        stat3, cat_id_list = get_list_val('cat_id', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = cat_id_list
        if stat1 and stat2 and stat3:
            res = users.handle_rss(uid, cat_id_list, opt)
            prod['rescode'] = res['rescode']

    elif tid == mock_data.type_dict['my_rss']:
        stat, uid = get_int_val('uid', request)
        if not stat:
            prod['rescode'] = 1
            prod['err'] = uid
        res = users.get_my_rss(uid)
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['rss_homepage']:
        stat1, uid = get_int_val('uid', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = uid
        stat2, page = get_int_val('page', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = page
        stat3, page_max_cnt = get_int_val('page_max_cnt', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = page_max_cnt
        if stat1 and stat2 and stat3:
            res = users.get_rss_homepage(uid, page, page_max_cnt)
            for k,v in res.items():
                prod[k] = v

    elif tid == mock_data.type_dict['my_fav']:
        stat, uid = get_int_val('uid', request)
        if not stat:
            prod['rescode'] = 1
            prod['err'] = uid
        res = users.get_my_fav(uid)
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['handle_fav']:
        stat1, uid = get_int_val('uid', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = uid
        stat2, opt = get_int_val('opt', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = opt
        stat3, fav_id = get_str_val('fav_id', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = fav_id
        stat4, doc_id = get_str_val('doc_id', request)
        if not stat4:
            prod['rescode'] = 1
            prod['err'] = doc_id
        if stat1 and stat2 and stat3 and stat4:
            res = users.handle_fav(uid, opt, fav_id, doc_id)
            for k,v in res.items():
                prod[k] = v

    elif tid == mock_data.type_dict['handle_fav_set']:
        stat1, uid = get_int_val('uid', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = uid
        stat2, opt = get_int_val('opt', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = opt
        if stat1 and stat2:
            stat, fav_id = get_str_val('fav_id', request)
            stat, fav_name = get_str_val('fav_name', request)
            res = users.handle_fav_set(uid, opt, fav_name, fav_id)
            for k,v in res.items():
                prod[k] = v        
 
    elif tid == mock_data.type_dict['search']:
        stat1, query = get_str_val('query', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = query
        stat2, page = get_int_val('page', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = page
        stat3, page_max_cnt = get_int_val('page_max_cnt', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = page_max_cnt
        if stat1 and stat2 and stat3:
            res = news.get_query(query, page, page_max_cnt)
            for k,v in res.items():
                prod[k] = v

    elif tid == mock_data.type_dict['source_guide']:
        res = news.get_source()
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['source_homepage']:
        stat1, source_name = get_str_val('source_name', request)
        if not stat1:
            prod['rescode'] = 1
            prod['err'] = query
        stat2, page = get_int_val('page', request)
        if not stat2:
            prod['rescode'] = 1
            prod['err'] = page
        stat3, page_max_cnt = get_int_val('page_max_cnt', request)
        if not stat3:
            prod['rescode'] = 1
            prod['err'] = page_max_cnt
        if stat1 and stat2 and stat3:
            res = news.get_source_homepage(source_name, page, page_max_cnt)
            for k,v in res.items():
                prod[k] = v

    elif tid == mock_data.type_dict['handle_share']:
        stat, doc_id = get_str_val('doc_id', request)
        if not stat:
            prod['rescode'] = 1
            prod['err'] = doc_id
        if stat:
            res = news.handle_share(doc_id)
            for k,v in res.items():
                prod[k] = v

    elif tid == mock_data.type_dict['handle_like']:
        stat, doc_id = get_str_val('doc_id', request)
        if not stat:
            prod['rescode'] = 1
            prod['err'] = doc_id
        if stat:
            res = news.handle_like(doc_id)
            for k,v in res.items():
                prod[k] = v

    return HttpResponse(json.dumps(prod, ensure_ascii=False))

def handle_request(request):
    tid = int(request.GET.get('type', -1))
    print 'tid ' + str(tid)
    qid = request.GET.get('qid', -1)
    if qid == -1:
        prod = {}
        prod['rescode'] = 1
        prod['err'] = 'No qid'
        return HttpResponse(json.dumps(prod, ensure_ascii=False))
    if qid == 'mock':
        prod = mock_data.mock_data[tid]
        return HttpResponse(json.dumps(prod, ensure_ascii=False))
    return normal_work(tid, qid, request)
