#!/usr/bin/env python
# encoding: utf-8
import traceback
import os
import sys
import scrapy
reload(sys)
sys.setdefaultencoding('utf-8')
import utils

def handle_father_cat(div):
    father_cat = div.xpath('./h1/span/a/text()')[0].extract()
    print 'father:' + father_cat
    return father_cat

def handle_sub_cat(father_cat, fcat_id, div):
    scat_id = 1
    for a in div.xpath('./div[@class="m920 left"]/a'):
        url = a.xpath('./@href')[0].extract().strip()
        sub_cat = a.xpath('./text()')[0].extract().strip()
        sub_id = fcat_id + scat_id
        line = '%d,%s,%d,%s,%s' % (fcat_id, father_cat, sub_id, sub_cat, url)
        print line
        scat_id += 1
        with open('cats.csv','a') as cat_file:
            print >> cat_file, line

def generate_cats(site_url):
    hxs = scrapy.Selector(text=utils.get_html_by_urllib(site_url))
    fcat_id = 1
    for div in hxs.xpath("//div[@class='m958 left border_blue']"):
        try:
            father_cat = handle_father_cat(div)
            handle_sub_cat(father_cat, fcat_id * 10000, div)
            fcat_id += 1
        except:
            traceback.print_exc()

if __name__ == '__main__':
    generate_cats('http://www.eol.cn/sitemap/')
