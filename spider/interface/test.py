# -*- coding:utf-8 -*-

import requests

payload = {
    'title':'test title',
    'source':'test source',
    'detail_url':'test',
    'create_time':'test',
    'cat_name':'test',
    'author':'test',
    'publish_time':'test',
    'text':'test',
}

r = requests.post('http://121.196.226.177:9090/di/', data=payload)
print r.text
