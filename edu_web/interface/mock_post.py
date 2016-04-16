import requests
import json

post_data = {
    'type':11,
    'qid':123,
    'uid':10001,
    'opt':0,
    'cat_list':[10001,10002],
}

url = 'http://121.196.226.177:8080/edu/'

req = requests.post(url, data=json.dumps(post_data))
import pdb
pdb.set_trace()
