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

import nltk
from nltk.corpus import stopwords

import MeCab

from collections import Counter

from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *
from KindleReferencedIndexScoreDBsSnapshotDealer import *
from KindleReferencedIndexScoreTFIDFUtils import *

import signal
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
    signal.signal(signal.SIGINT, exit_gracefully)

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
def tokenize_all(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(lambda t:t != '' and t != None, texts)
    build_text    = ' '.join(visible_texts).replace('\n', '')
    MT= MeCab.Tagger('mecabrc')
    res = MT.parse(build_text.encode('utf-8') )
    items = stamming(res)
    counter = Counter(stamming(res))
    tf      = filter(lambda x:not x[0] in STOPWORDS, sorted([(term, float(val)) for term, val in counter.items()], key=lambda x:x[1]*(-1) )  )
    return dict(tf)

"""
Kindle Unlimited的な要素を探す
"""
def is_kindle_unlimited(soup):
    boxs = soup.findAll('a', {'id': re.compile('kuInfo') } )
    if boxs == []:
      return None
    #print(boxs[0].text, 'Kindle Unlimited'.decode('utf-8') in boxs[0].text )
    #print(boxs[0].text, re.search( '(Kindle Unlimited.*?お楽しみいただけます)'.decode('utf-8'), boxs[0].text, re.UNICODE).groups() )
    return  len(re.search( '(Kindle Unlimited.*?お楽しみいただけます)'.decode('utf-8'), boxs[0].text, re.UNICODE).groups() )

import msgpack
def make_keyurl_Tindex(scraping_data):
    soup = bs4.BeautifulSoup(str(scraping_data.html))
    asin = scraping_data.asin
    is_unlimited = is_kindle_unlimited(soup)
    tf        = tokenize_all(soup)
    tindexdb = plyvel.DB('./' + CM.DEFAULT_TINDEX_URL_TERM, create_if_missing=True)
    if is_unlimited:
      tf.update( {'[@ThisIsKindleUnlimited]': 1} )
      print('[INFO] Kindle Unlimited Found')
    for t,f in  tf.items():
      idfw =  idfdic.get(t)
      """
      未知語の場合、最大サイズを利用
      """
      if not idfw:
        idfw = defaultidfsize
      line = tindexdb.get(t)
      if line == None:
        tindexdb.put(t, msgpack.packb( {asin: f*idfw} ) )
      else:
        dic = msgpack.unpackb(line)
        if dic.get(asin):
          dic[asin] = f*idfw
        else:
          dic.update( {asin: f*idfw} )
        tindexdb.put(t, msgpack.packb( dic ) )
    
    tindexdb.close()

def Tindex_dumper():
    tindexdb = plyvel.DB('./' + CM.DEFAULT_TINDEX_URL_TERM, create_if_missing=True)
    for k, v in tindexdb:
        d = msgpack.unpackb(v)
        print(k, ' '.join([x + '/' + str(y) for x,y in d.items()]) )
"""
load default idf dictionary to memory
"""
idfdic = {}
defaultidfsize = 0.
with open(CM.DEFAULT_IDFDIC, 'r') as f:
  lines = filter(lambda x:x!='', f.read().split('\n'))
  defaultidfsize = float(lines[-1].split(' ').pop() )
  for line in lines:
    weight = float(line.split(' ').pop())
    term   = ' '.join(line.split(' ')[:-1])
    #print(line)
    #print(word, '___', weight)
    idfdic.update( {term: weight} )
  print('[INFO] Finish load idfdic...')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--mode',   help='You can specify DB, which local or SQL.')
    parser.add_argument('--refresh', help='You can choose refresh new db or use old db.')
    args_obj = vars(parser.parse_args())

    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    mode                    = args_obj.get('mode')
    refresh                 = args_obj.get('refresh') 
    if mode and mode == 'level':
        if refresh == None or refresh.lower() == 'false':
            pass
        else:
            MySQLWrapper.dump2leveldb(CM.LEVELDB_SHADOW_TINDEX)
        for _, scraping_data in enumerate(SnapshotDeal.get_all_ldb() ):
            make_keyurl_Tindex(scraping_data)
            print('[INFO] Now analyzing ...', _ )
    if mode and mode == 'dump':
        Tindex_dumper()
