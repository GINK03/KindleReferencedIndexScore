# coding: utf-8
# transit
from __future__ import print_function
import bs4
import plyvel
import sys
import urllib2
import urllib
import os.path
import argparse
from datetime import datetime
import re
import hashlib
import KindleReferencedIndexScoreTinyDBConnector

import regex

import nltk
from nltk.corpus import stopwords

import MeCab

from collections import Counter

from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *
from KindleReferencedIndexScoreDBsSnapshotDealer import *
from KindleReferencedIndexScoreTFIDFUtils import *

NUMBER_PATTERN = r'[+-]?\d+(?:\.\d+)?' 
NUMBER_REGEX = re.compile(r'[+-]?\d+(?:\.\d+)?')

STOPWORDS = map(lambda x:x, 'abcdejghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.?:')
nltk.download('stopwords')
STOPWORDS.extend( stopwords.words('english') )

"""
以下のGITHUBIOを参考に、日本語のストップワードを拡張。
http://github.com/pika-shi/sphinx_information_retrieval/blob/master/natural_language_processing.rst
TODO: 必要に応じて、増やしていく
"""
STOPWORDS.extend('あそこ,あたり,あちら,あっち,あと,あな,あなた,あれ,いくつ,いつ,いま,いや,いろいろ,うち,おおまか,おまえ,おれ,がい,かく,かたち,かやの,から,がら,きた,くせ,ここ,こっち,こと,ごと,こちら,ごっちゃ,これ,これら,ごろ,さまざま,さらい,さん,しかた,しよう,すか,ずつ,すね,すべて,ぜんぶ,そう,そこ,そちら,そっち,そで,それ,それぞれ,それなり,たくさん,たち,たび,ため,だめ,ちゃ,ちゃん,てん,とおり,とき,どこ,どこか,ところ,どちら,どっか,どっち,どれ,なか,なかば,なに,など,なん,はじめ,はず,はるか,ひと,ひとつ,ふく,ぶり,べつ,へん,ぺん,ほう,ほか,まさ,まし,まとも,まま,みたい,みつ,みなさん,みんな,もと,もの,もん,やつ,よう,よそ,わけ,わたし,ハイ,上,中,下,字,年,月,日,時,分,秒,週,火,水,木,金,土,国,都,道,府,県,市,区,町,村,各,第,方,何,的,度,文,者,性,体,人,他,今,部,課,係,外,類,達,気,室,口,誰,用,界,会,首,男,女,別,話,私,屋,店,家,場,等,見,際,観,段,略,例,系,論,形,間,地,員,線,点,書,品,力,法,感,作,元,手,数,彼,彼女,子,内,楽,喜,怒,哀,輪,頃,化,境,俺,奴,高,校,婦,伸,紀,誌,レ,行,列,事,士,台,集,様,所,歴,器,名,情,連,毎,式,簿,回,匹,個,席,束,歳,目,通,面,円,玉,枚,前,後,左,右,次,先,春,夏,秋,冬,一,二,三,四,五,六,七,八,九,十,百,千,万,億,兆,下記,上記,時間,今回,前回,場合,一つ,年生,自分,ヶ所,ヵ所,カ所,箇所,ヶ月,ヵ月,カ月,箇月,名前,本当,確か,時点,全部,関係,近く,方法,我々,違い,多く,扱い,新た,その後,半ば,結局,様々,以前,以後,以降,未満,以上,以下,幾つ,毎日,自体,向こう,何人,手段,同じ,感じ'.split(',') )
STOPWORDS.extend(['。', '、', 'を', 'の', 'に', 'お', 'で', 'し', 'が', 'て', 'は', 'です', 'ます'])

"""
mecabからのデータをstammingするデータエンジン
"""
def stamming(raw):
    items = []
    for line in str(raw).split('\n'):
      if len(line.split(',')) < 3:
        continue
      head = line.split('\t').pop(0).lower()  
      stam = line.split(',')[-3].lower()
      if stam =='*':
        items.append( head )
      else:
        items.append( '[' + stam + ']' )
    return items
"""
全要素の形態素解析
textデータの抜出と、余計な情報の削除
"""
def tokenize_flatten_list(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(lambda t:t != '' and t != None, texts)
    build_text    = ' '.join(visible_texts).replace('\n', '')
    MT= MeCab.Tagger('mecabrc')
    res = MT.parse(build_text.encode('utf-8') )
    items = stamming(res)
    return items

import msgpack
def make_flatten_list(scraping_data):
    asin = scraping_data.asin
    line = scraping_data.html.replace('\n', '')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('', '\n')
    
    soup = bs4.BeautifulSoup(html)
    flatten_list   = tokenize_flatten_list(soup)
    return msgpack.packb(flatten_list)

if __name__ == '__main__':
    asins = list()
    #parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    #args_obj = vars(parser.parse_args())
    
    if '-d' in sys.argv:
       for k, v in plyvel.DB('./tmp/word2vec_corpus.ldb' , create_if_missing=True):
         print(k, v) 
    
    if '-a' in sys.argv:
	db = plyvel.DB('./tmp/word2vec_corpus.ldb', create_if_missing=True)
	for _, (keyurl, scraping_data) in enumerate(get_all_data_iter() ):
	    if db.get(keyurl):
                print('[INFO] ', _, keyurl, 'will be passed!')
		continue
	    line = make_flatten_list(scraping_data) 
	    print(_, keyurl, line)
	    db.put(keyurl, line)
	db.close()
