# -*- coding: utf-8 -*-
__author__ = 'Sequoia Yang'

import Queue
import httplib,urllib
import re
import os

url_pattern = "/hs/info/card_zhcn/"

class LushiImageFetcher(object):
    @staticmethod
    def fetch_html(page):
        # extract a valid address
        host = page.split('/')[0]
        url = '/'.join(page.split('/')[1:]) if len( page.split('/')) > 1 else ''
        headers = {"Host": host,
                   "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                    "Accept": "text/plain"}

        http_client = httplib.HTTPConnection(host)
        http_client.request('GET', '/' + url, headers=headers )
        response = http_client.getresponse()
        #print response.status, host + '/' + url
        if response.status != 200:
            response.read()
            return None
        s = response.read()
        s = s.replace("\r\n"," ")
        return s

    @staticmethod
    def extract_title(html):
        result = re.findall(r"<div class=\"head\" name=\"Title_.*?\">.*<h1>(.*?)<span class=", html, re.S)
        return result[0].decode('GBK')

    # get the links from the product page , pointing to another card
    @staticmethod
    def get_other_cards(card_id):
        html = LushiImageFetcher.fetch_html("cha.17173.com/hs/info/card_zhcn/" + str(card_id))
        if html == None or len(html) == 0:
            return []
        out_file = 'html/' + card_id
        out_file = open(out_file, 'w')
        out_file.write(html)
        out_file.close()
        results = re.findall(url_pattern + '(\d+)', html)
        return [a for a in list(set(results))]

    @staticmethod
    def get_all_cards_id():
        all_cards = set()
        q = Queue.Queue()
        q.put('120')
        while not q.empty():
            card = q.get()
            for other in filter(lambda card:card not in all_cards, LushiImageFetcher.get_other_cards(card)):
                q.put(other)
                all_cards.add(other)
                print len(all_cards), '---', other

    @staticmethod
    def get_all_cards():
        #LushiImageFetcher.get_all_cards_id()
        count = 0
        for i in range(0,1000):
            try:
                if not os.path.exists('html/' + str(i)):
                    LushiImageFetcher.get_other_cards(str(i))
                    count += 1
                    print count
            except Exception:
                pass
    @staticmethod
    def get_images():
        for root,dirs,files in os.walk('html/'):
            for filespath in files:
                html = open('html/' + filespath).read()
                result = re.findall(r"images/resource/card_zhcn/(.*?).png", html, re.S)
                print filespath,result
        return "i2.17173cdn.com/8hpoty/YWxqaGBf/images/resource/card_zhcn/" + result[0] + ".png"


for image in LushiImageFetcher.get_images():
    print image
        
