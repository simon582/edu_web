# -*- coding:utf-8 -*-

import sys
sys.path.append('../comm/')
import utils
import scrapy
from bs4 import BeautifulSoup
import time
import datetime
import pymongo
import traceback
import hashlib
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')

conn = pymongo.MongoClient()
news_table = conn['edu']['news']

def save(prod):
    news_table.save(prod)

def doc_crawled(doc_id):
    return news_table.count({'doc_id':doc_id}) > 0


def crawl_detail(prod, detail_url):
    page = 0
    while 1:
        if page == 0:
            cur_url = detail_url
        else:
            cur_url = detail_url.split('.shtml')[0] + '_%d.shtml' % page
        #print 'cur_detail_url:' + cur_url
        html = utils.get_html_by_urllib(cur_url)
        soup = BeautifulSoup(html)
        text_list = soup.find_all("div", class_="TRS_Editor")
        if len(text_list) == 0:
            break
        for s in text_list[0].strings:
            s = s.strip()
            if s == '':
                continue
            prod['text'].append(s)
            find_content = True
            #print s
        page += 1
    
def handle_detail_url(prod, start_url):
    if prod['detail_url'].find('http://') != -1:
        return
    cnt = 0
    for c in prod['detail_url']:
        if c == '.':
            cnt += 1
        else:
            break
    prefix_url = '/'.join(start_url.split('/')[0:len(res) - cnt])
    prod['detail_url'] = prefix_url + prod['detail_url'][cnt:]

def crawl_list_1(cat_info, start_url):
    hxs = scrapy.Selector(text=utils.get_html_by_urllib(start_url))
    for li in hxs.xpath('//div[@class="page_left"]/ul/li'):
        try:
            prod = {}
            for k,v in cat_info.items():
                prod[k] = v
            prod['source'] = 'eol'
            prod['author'] = '中国教育在线'
            prod['title'] = li.xpath('./a/text()')[0].extract()
            prod['doc_id'] = hashlib.md5(prod['title']).hexdigest().upper()
            prod['datetime'] = li.xpath('./span/text()')[0].extract()
            if doc_crawled(prod['doc_id']):
                return
            if not utils.valid_title(prod['title']):
                continue
            prod['detail_url'] = li.xpath('./a/@href')[0].extract()
            handle_detail_url(prod, start_url)
            prod['text'] = []
            crawl_detail(prod, prod['detail_url'])
            prod['createtime'] = datetime.datetime.now()
            save(prod)
            utils.alog('NOTICE', 'crawl doc:' + prod['doc_id'])    
        except:
            utils.alog('WARN', 'Cannot crawl doc:' + prod['detail_url'])
            traceback.print_exc()

if __name__ == "__main__":
    with open('cats.csv') as cat_file:
        for line in cat_file.readlines():
            prod = {}
            res = line.strip().split(',')
            prod['father_id'] = int(res[0])
            prod['father_name'] = res[1]
            prod['cat_id'] = int(res[2])
            prod['cat_name'] = res[3]
            start_url = res[4]
            try:
                crawl_list_1(prod, start_url)
            except:
                utils.alog('ERROR', 'Cannot crawl cat:' + start_url)
            utils.alog('NOTICE', start_url + ' crawl finished')
