# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import mock_data
from django.http import HttpResponse
import json
sys.path.append('./edu_web/interface')
import data
import users
from django.views.decorators.csrf import csrf_exempt

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
    prod = {}
    stat, prod['qid'] = get_str_val('qid', request)
    if not stat:
        return HttpResponse(prod['qid'])

    if tid == mock_data.type_dict['welcome']:
        prod['img_url'] = ''

    elif tid == mock_data.type_dict['cat_guide']:
        prod['cat_list'] = data.get_cat_guide()

    elif tid == mock_data.type_dict['login']:
        stat, username = get_str_val('username', request)
        if not stat:
            return HttpResponse(username)
        stat, passwd = get_str_val('passwd', request)
        if not stat:
            return HttpResponse(passwd)
        res = users.login_user(username, passwd)
        for k,v in res.items():
            prod[k] = v       
 
    elif tid == mock_data.type_dict['register']:
        stat, username = get_str_val('username', request)
        if not stat:
            return HttpResponse(username)
        stat, passwd = get_str_val('passwd', request)
        if not stat:
            return HttpResponse(passwd)
        stat, category = get_int_val('category', request)
        if not stat:
            return HttpResponse(category)
        stat, data = get_str_val('data', request)
        if not stat:
            return HttpResponse(data)
        
        res = users.register_user(username, passwd, category, data)
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['cat_homepage']:
        stat, cat_id = get_int_val('cat_id', request)
        if not stat:
            return HttpResponse(cat_id)
        stat, page = get_int_val('page', request)
        if not stat:
            return HttpResponse(page)
        stat, page_max_cnt = get_int_val('page_max_cnt', request)
        if not stat:
            return HttpResponse(page_max_cnt)
        res = data.get_cat_homepage(cat_id, page, page_max_cnt)
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['news_homepage']:
        stat, doc_id = get_str_val('doc_id', -1)
        if not stat:
            return HttpResponse(doc_id)
        res = data.get_news_homepage(doc_id)
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['my_homepage']:
        prod['portrait_url'] = ''
        prod['others'] = ''

    elif tid == mock_data.type_dict['handle_rss']:
        stat, uid = get_int_val('uid', request)
        if not stat:
            return HttpResponse(uid)
        stat, opt = get_int_val('opt', request)
        if not stat:
            return HttpResponse(opt)
        stat, cat_id_list = get_list_val('cat_id', request)
        if not stat:
            return HttpResponse(cat_id_list)
        res = users.handle_rss(uid, cat_id_list, opt)
        prod['rescode'] = res['rescode']
    return HttpResponse(json.dumps(prod, ensure_ascii=False))

@csrf_exempt
def handle_request(request):
    tid = int(request.GET.get('type', -1))
    print 'tid ' + str(tid)
    qid = request.GET.get('qid', -1)
    if qid == -1:
        return HttpResponse('No qid')
    if qid == 'mock':
        prod = mock_data.mock_data[tid]
        return HttpResponse(json.dumps(prod, ensure_ascii=False))
    return normal_work(tid, qid, request)
