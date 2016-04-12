#!/usr/bin/env python
# encoding: utf-8
import requests
import datetime
import time
import urllib
import urllib2
import cookielib
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ban_list = [
    '试题',
    '真题',
    '答案',
    '原题',
]

def valid_title(text):
    global ban_list
    for ban_word in ban_list:
        if text.find(ban_word) != -1:
            return False
    return True

def get_html_by_urllib(url):
    data = {}
    post_data = urllib.urlencode(data)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36')
    f = opener.open(req, timeout = 10)
    html = f.read().decode('gbk')
    html_file = open('test.html', 'w')
    print >>html_file, html
    f.close()
    return html

'''
    level details (from top to bottom) :
        ERROR
        WARN
        NOTICE
        DEBUG
'''
log_level = {
    'DEBUG' : 0,
    'NOTICE' : 1,
    'WARN' : 2,
    'ERROR' : 3
}
output_threshold = 'DEBUG'

def alog(level, log_text, screen = True, log_path = '/data/edu/spider_log/'):
    if log_level[level] < log_level[output_threshold]:
        return
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    cur_day = str(datetime.datetime.now()).split(' ')[0]
    file_path = log_path + 'spider.%s.log' % cur_day
    cur_time = str(datetime.datetime.now()).split('.')[0]
    outline = '[%s][%s]%s' % (cur_time, level, log_text)
    if screen:
        print outline
    with open(file_path, 'a') as log_file:
        print >> log_file, outline

if __name__ == '__main__':
    get_html_by_urllib('http://www.eol.cn/sitemap/')
