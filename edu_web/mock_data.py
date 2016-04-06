# -*- coding:utf-8 -*-

import random

def generate_enum_dict(type_list):
    type_dict = {}
    for tid in xrange(len(type_list)):
        type_dict[type_list[tid]] = tid
    return type_dict

mock_data = {}

type_list = [
    'welcome',                  #0 
    'login',                    #1
    'register',                 #2
    'cat_guide',                #3
    'news_homepage',            #4
    'cat_homepage',             #5
    'my_homepage',              #6
    'search',                   #7
    'my_fav',                   #8
    'handle_fav',               #9
    'my_rss',                   #10
    'handle_rss',               #11
    'source_guide',             #12
    'source_homepage',          #13
    'rss_homepage',             #14
    'handle_share',             #15
    'handle_like',              #16
]
type_dict = generate_enum_dict(type_list)

'''=====================欢迎模块====================='''

welcome_request = {
    "type":type_dict['welcome'],
    "qid":"mock"
}

welcome_response = {
    "qid":"mock",
    "img_url":"https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/bd_logo1_31bdc765.png",
}

mock_data[type_dict['welcome']] = welcome_response

'''=====================登录模块====================='''

user_cat_list = [
    'wechat',
    'weibo',
    'qq',
    'phone',
]
login_cat_dict = generate_enum_dict(user_cat_list)

login_request = {
    "type":type_dict['login'],
    "qid":"mock",
    "username":"testname",
    "passwd":"123456",
    "category":login_cat_dict['phone'],
}

res_code_list = [
    'success',
    'wrong_username_or_password',
    'user_not_exist',
    'user_is_exist',
    'fav_handle_success',
    'fav_handle_fail',
    'rss_handle_success',
    'rss_handle_fail',
]
res_code_dict = generate_enum_dict(res_code_list)

login_response = {
    "qid":"mock",
    "rescode":res_code_dict['success'],
    "username":"mockname",
    "uid":111222,
    "others":"",
}

mock_data[type_dict['login']] = login_response

'''=====================注册模块====================='''

register_request = {
    "type":type_dict['register'],
    "qid":"mock",
    "username":"mockname",
    "passwd":"123456",
    "data":"location=Hangzhou&sex=Male",
    "category":login_cat_dict['phone'],
}

register_response = {
    "qid":"mock",
    "rescode":res_code_dict['user_is_exist'],
    "username":"mockname",
    "uid":111222,
    "others":"",
}

mock_data[type_dict['register']] = register_response

'''=====================引导分类模块====================='''

cat_guide_request = {
    "type":type_dict['cat_guide'],
    "qid":"mock",
}

cat_example = {
    "cat_id":123,
    "title":"初中",
    "sub_title":"中考",
    "sub_cat":[
        {
            "cat_id":"123001",
            "title":"中考",
            "last_title":"最新中考资讯大全",
            "last_modify":"2016-03-26 23:00",
            "bg_image":"http://test.image.com",
        },
    ],
}

cat_guide_response = {
    "qid":"mock",
    "cat_list":[cat_example,cat_example,cat_example],
}

mock_data[type_dict['cat_guide']] = cat_guide_response

'''=====================分类主页模块====================='''

cat_homepage_request = {
    "type":type_dict['cat_homepage'],
    "qid":"mock",
    "cat_id":"123",
    "page":1,
    "page_max_cnt":10,
}

doc_example = {
    "doc_id":12321,
    "title":"中考",
    "author":"mockauthor",
    "datetime":"2016-03-20 20:00:00",
    "source":"Sina",
    "bg_image":"http://background.image.com/",
    "text":"This is sample text",
    "source_icon":"http://icon.image.com/",
    "source_desc":"百度",
    "share_cnt":22,
    "collection_cnt":88,
    "like_cnt":100,
}

example_doc_list = []
for i in xrange(10):
    example_doc_list.append(doc_example)

cat_homepage_response = {
    "qid":"mock",
    "end":random.choice([0,1]),
    "doc_list":example_doc_list,
}

mock_data[type_dict['cat_homepage']] = cat_homepage_response

'''=====================新闻内容模块====================='''

res_code_dict = generate_enum_dict(res_code_list)

news_homepage_request = {
    "type":type_dict['news_homepage'],
    "qid":"mock",
    "doc_id":123,
    #type=cat&cat_id=321 or type=fav&fav_id=111 or type=source&source_name=sina
    "list_desc":"type=rss&uid=111",
}

news_homepage_response = {
    "qid":"mock",
    "text":'aaaaa<br>bbbbb<br><img src="http://text.image.com/" width=200 height=500>ccccc<br>',
    "base":doc_example,
    "pre_id":122,
    "next_id":124,
}

mock_data[type_dict['news_homepage']] = news_homepage_response

'''=====================我的主页模块====================='''

my_homepage_request = {
    "type":type_dict['my_homepage'],
    "qid":"mock",
    "uid":111222,
}

my_homepage_response = {
    "qid":"mock",
    "portrait_url":"http://portrait.image.com",
    "others":"",
}

mock_data[type_dict['my_homepage']] = my_homepage_response

'''=====================搜索发现模块====================='''

search_request = {
    "type":type_dict['search'],
    "qid":"mock",
    "query":"中考",
    "page":1,
    "page_max_cnt":10,
}

search_response = {
    "qid":"mock",
    "end":random.choice([0,1]),
    "doc_list":example_doc_list,
}

mock_data[type_dict['search']] = search_response

'''=====================收藏模块====================='''

fav_example = {
    "fav_id":333,
    "uid":111222,
    "fav_name":"中考教育",
    "doc_list":example_doc_list,
    "fav_icon":"http://icon.fav.com",    
}

my_fav_request = {
    "type":type_dict['my_fav'],
    "qid":"mock",
    "uid":111222, 
}

my_fav_response = {
    "qid":"mock",
    "fav_list":[fav_example,fav_example,fav_example],
}

mock_data[type_dict['my_fav']] = my_fav_response

opt_list = [
    'add',
    'remove',
]
opt_dict = generate_enum_dict(opt_list)

handle_fav_request = {
    "type":type_dict['handle_fav'],
    "qid":"mock",
    "opt":opt_dict['add'],
    "uid":111222,
    "fav_id":333,
    "doc_id":123,
}

handle_fav_response = {
    "qid":"mock",
    "rescode":res_code_dict['fav_handle_success'],
}

mock_data[type_dict['handle_fav']] = handle_fav_response

'''=====================订阅模块====================='''

my_rss_request = {
    "type":type_dict['my_rss'],
    "qid":"mock",
    "uid":111222, 
}


rss_cat_example = {
    "cat_id":"123001",
    "title":"中考",
    "last_title":"最新中考资讯大全",
    "last_modify":"2016-03-26 23:00",
    "bg_image":"http://test.image.com",
}

my_rss_response = {
    "qid":"mock",
    "cat_list":[rss_cat_example, rss_cat_example, rss_cat_example],
}

mock_data[type_dict['my_rss']] = my_rss_response

handle_rss_request = {
    "type":type_dict['handle_rss'],
    "qid":"mock",
    "opt":opt_dict['add'],
    "uid":111222,
    "cat_id":[111,222,333],
}

handle_rss_response = {
    "qid":"mock",
    "rescode":res_code_dict['rss_handle_success'],
}

mock_data[type_dict['handle_rss']] = handle_rss_response

rss_homepage_request = {
    "type":type_dict['rss_homepage'],
    "qid":"mock",
    "uid":111222, 
    "page":1,
    "page_max_cnt":10,
}

rss_homepage_response = {
    "qid":"mock",
    "end":random.choice([0,1]),
    "doc_list":example_doc_list,
}

mock_data[type_dict['rss_homepage']] = rss_homepage_response

'''=====================新闻源模块====================='''

source_guide_request = {
    "type":type_dict['source_guide'],
    "qid":"mock",
}

source_example = {
    'source':'sina',
    'source_desc':'新浪新闻',
    'source_icon':'http://icon.image.com/',
    "last_title":"最新中考资讯大全",
    "last_modify":"2016-03-26 23:00",
    "bg_image":"http://test.image.com",
}

source_guide_response = {
    "qid":"mock",
    "source_list":[source_example, source_example, source_example],
}

mock_data[type_dict['source_guide']] = source_guide_response

source_homepage_request = {
    "type":type_dict['source_homepage'],
    "qid":"mock",
    "source_name":"Sina",
    "page":1,
    "page_max_cnt":10,
}

source_homepage_response = {
    "qid":"mock",
    "end":random.choice([0,1]),
    "doc_list":example_doc_list,
}

mock_data[type_dict['source_homepage']] = source_homepage_response

'''=====================分享统计模块====================='''

handle_share_request = {
    "type":type_dict['handle_share'],
    "qid":"mock",
    "doc_id":100001,
}

handle_share_response = {
    "qid":"mock",
    "rescode":0,
}

mock_data[type_dict['handle_share']] = handle_share_response

'''=====================点赞统计模块====================='''

handle_like_request = {
    "type":type_dict['handle_like'],
    "qid":"mock",
    "doc_id":100001,
}

handle_like_response = {
    "qid":"mock",
    "rescode":0,
}

mock_data[type_dict['handle_like']] = handle_like_response
