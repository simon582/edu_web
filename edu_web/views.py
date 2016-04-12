# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import mock_data
from django.http import HttpResponse
import json
sys.path.append('./edu_web/interface')
import data

def get_int_val(key_name, request):
    try:
        val = int(request.GET.get(key_name, -1))
        if val == -1:
            return HttpResponse('no ' + key_name)
    except:
        return HttpResponse('invalid ' + key_name)
    return val

def normal_work(tid, qid, request):
    prod = {}
    prod['qid'] = request.GET.get('qid', -1)

    if tid == mock_data.type_dict['cat_guide']:
        prod['cat_list'] = data.get_cat_guide()

    elif tid == mock_data.type_dict['cat_homepage']:
        cat_id = get_int_val('cat_id', request)
        page = get_int_val('page', request)
        page_max_cnt = get_int_val('page_max_cnt', request)
        res = data.get_cat_homepage(cat_id, page, page_max_cnt)
        for k,v in res.items():
            prod[k] = v

    elif tid == mock_data.type_dict['news_homepage']:
        doc_id = request.GET.get('doc_id', -1)
        res = data.get_news_homepage(doc_id)
        for k,v in res.items():
            prod[k] = v

    return HttpResponse(json.dumps(prod, ensure_ascii=False))

def handle_request(request):
    tid = int(request.GET.get('type', 0))
    print 'tid ' + str(tid)
    qid = request.GET.get('qid', -1)
    if qid == -1:
        return HttpResponse('No qid')
    if qid == 'mock':
        prod = mock_data.mock_data[tid]
        return HttpResponse(json.dumps(prod, ensure_ascii=False))
    return normal_work(tid, qid, request)
