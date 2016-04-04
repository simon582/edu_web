#!/usr/bin/env python
# encoding: utf-8
import requests
import urllib
import urllib2
import cookielib
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_html_by_urllib(url):
    data = { }
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

if __name__ == '__main__':
    get_html_by_urllib('http://www.eol.cn/sitemap/')
