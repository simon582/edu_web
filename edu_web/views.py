# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import mock_data
from django.http import HttpResponse
import json

def handle_request(request):
    tid = int(request.GET.get('type', 0))
    print 'tid ' + str(tid)
    return HttpResponse(json.dumps(mock_data.mock_data[tid], ensure_ascii=False))
