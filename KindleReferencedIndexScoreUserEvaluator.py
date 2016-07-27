# coding: utf-8
from __future__ import print_function
import bs4
import sys
import urllib2
import urllib
import os.path
import __future__
import argparse
from datetime import datetime
import re
import hashlib
import KindleReferencedIndexScoreTinyDBConnector

import MeCab

from collections import Counter

from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *
from KindleReferencedIndexScoreDBsSnapshotDealer import *
from KindleReferencedIndexScoreTFIDFUtils import *



NUMBER_PATTERN = r'[+-]?\d+(?:\.\d+)?' 
NUMBER_REGEX = re.compile(r'[+-]?\d+(?:\.\d+)?')


STOPWORDS = map(lambda x:x, 'abcdejghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.?:')
STOPWORDS.extend(['。', '、', 'を', 'の', 'に', 'お', 'で', 'し', 'が', 'て', 'は', 'です', 'ます'])
STOPLOGIC = (lambda x:len(x[0]) > 3 )

def ranking_logic():
    a, b = 0.5, 0.5


def referenced_score(scraping_data_list):
    source_list = filter(lambda x:len(x[1].evaluated) != 0, sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1) )
    #source_list = sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1)
    for (url, scraping_data) in source_list:
        print(scraping_data.url, scraping_data, map(lambda x:x.from_url, scraping_data.evaluated) )

"""
レビューの調和平均の計算
"""
def calculate_harmonic_mean(reviews):
    size        = len(reviews)
    hsource     = map(lambda x:(float(x.star),float(x.vote)), reviews)
    #print('hsource', hsource)
    sigma       = sum( map(lambda x:x[1], hsource) )
    #print('sigma', sigma)
    inverted    = sum( map(lambda x:x[1]/x[0], hsource) )
    #print('inverted', inverted)
    score       = sigma/( (lambda x:x if x != 0. else float('inf'))(inverted) )
    return score

"""
レビューの単純平均の計算
"""
def calculate_normal_mean(reviews):
    size        = len(reviews)
    hsource     = map(lambda x:float(x.star), reviews)
    sigma       = sum( map(lambda x:x, hsource) )
    inverted    = len( hsource )
    score       = sigma/( (lambda x:x if x != 0. else float('inf'))(inverted) )
    return score

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
    items = map(lambda x:x.split('\t').pop(0), str(res).split('\n'))
    counter = Counter(items)
    tf      = filter(lambda x:not x[0] in STOPWORDS, sorted([(term, float(val)) for term, val in counter.items()], key=lambda x:x[1]*(-1) )  )
    tf      = filter(STOPLOGIC, tf )
    for t, f in tf:
        #print(t,f)
        pass
    return tf

"""
レビューの形態素解析を行い、tfを取得する
"""
def tokenize_reviews(reviews_context):
    csource     = reviews_context
    #print('csource ', csource)
    MT= MeCab.Tagger('mecabrc')
    res = MT.parse(csource.encode('utf-8'))
    items       = map(lambda x:x.split('\t').pop(0), str(res).split('\n'))
    counter     = Counter(items)
    #print('res ', res)
    #print('counter', counter)
    tf          = filter(lambda x:not x[0] in STOPWORDS, sorted([(term, float(val)) for term, val in counter.items()], key=lambda x:x[1]*(-1) ) )
    tf          = filter(STOPLOGIC, tf )
    """
    ウェイトのノーマライズを行う
    TODO: IDFの採用のため、allweight = 1.で固定
    """
    allweight   = 1. #sum(map(lambda x:x[1], tf))
    tf          = map(lambda x:(x[0], x[1]/allweight), tf)
    return tf

"""
商品情報の取得と、形態素の取得
"""
def parse_productinfo(soup):
    box_divs = soup.findAll('div', {'id': re.compile('.*?feature_div*') } )
    productinfo = ' '.join( filter(lambda x:x!='', map(lambda div:div.text.replace('\n', '').replace(' ', ''), box_divs) ) )
   
    MT= MeCab.Tagger('mecabrc')
    res = MT.parse(productinfo.encode('utf-8') )
    items = map(lambda x:x.split('\t').pop(0), str(res).split('\n'))
    counter = Counter(items)
    tf      = filter(lambda x:not x[0] in STOPWORDS, sorted([(term, float(val)) for term, val in counter.items()], key=lambda x:x[1]*(-1) )  )
    tf      = filter(STOPLOGIC, tf )
    """
    ウェイトのノーマライズを行う 
    NOTE: IDFでは、ノーマライズは不要では？
    TODO: IDFを採用したいので、allweightはなしの方向で
    """
    allweight= 1. #sum(map(lambda x:x[1], tf))
    tf      = map(lambda x:(x[0], x[1]/allweight), tf)
    #for term, val in sorted([(term, val) for term, val in tf], key=lambda x:x[1]*(-1) ) :
    #    print(term,val)
    #    pass
    #print(tf)
    return (productinfo.encode('utf-8'), tf)
    #print( productinfo )

"""
星・レビューコンテキスト・vote数を取得し
Reviewのインスタンスreviewsを返却
"""
def parse_star_review_vote(soup):
    box_divs = soup.findAll('div', {'id': re.compile('rev-dpReviewsMostHelpfulAUI-*') } )
    
    if box_divs == [] or box_divs == None : 
        return [], ''
    
    stars = []
    for box_div in box_divs:
        starl = re.findall(NUMBER_REGEX, box_div.find('a', {'class': 'a-link-normal'} )['title'])
        #print(starl)
        star = starl.pop()
        stars.append(star)
    
    cr_votes = [] 
    for box_div in box_divs:
        cr_vote_text = (lambda x:x.pop(0) if x != [] else '0')(re.findall(NUMBER_REGEX, box_div.find('span', {'id' : re.compile('cr-vote-*') } ).text.replace('\n', '') ) )
        cr_votes.append( cr_vote_text )
    
    contexts = []
    context_wrap_divs = soup.findAll('div', {'id': re.compile('revData-dpReviewsMostHelpfulAUI-*') } )
    for context_wrap_div in context_wrap_divs:
        context = context_wrap_div.findAll('div', {'class': 'a-section'} ).pop(0).text.replace('\n', '')
        contexts.append(context) 

    """
    評価データを更新する
    """
    reviews = []
    for star, context, vote in zip(stars, contexts, cr_votes):
        #print(star, context, vote)
        review = Review()
        hashes = str(hashlib.sha224(context.encode('utf-8')).hexdigest())            
        (review.star, review.context, review.vote, review.hashes) = star, context, vote, hashes
        reviews.append(review)
    #print('review in inner', reviews)
    #print('review stars in inner', map(lambda x:x.star, reviews))
    return reviews, ' '.join(contexts)

"""
relevancyの計算
NOTE: tfidfに更新
"""
def calc_relevancy(sourcetf, targettf, top=None):
    relevancy = 0.
    count = 0
    relevancy_term = []
    for tf in sourcetf:
        res = (lambda x:x.pop() if x != [] else None)( filter(lambda x:tf[0] == x[0], targettf) )
        if res == [] or res == None: continue
        #relevancy += res[1] * tf[1] * (lambda x:x**2 if x else 1. )( IDFHolder.IDFs.get(tf[1]) )
        relevancy += IDFHolder.IDFs.get(tf[0]) * tf[1]
        relevancy_term.append(res[0] )
        count += 1
        #if top and top < cnt : break
    return (relevancy, count, relevancy_term )

def parse_eval_and_update(scraping_data):
    """
    すでに評価済みなら、処理しない
    """
    if is_already_analyzed(scraping_data) == True:
        print('[DEBUG] Already analyzed', scraping_data.asin)
        #return

    soup = bs4.BeautifulSoup(str(scraping_data.html))

    """
    kill all script and style elements
    """
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    """
    星・レビューコンテキスト・vote数を取得し
    x.reviewsのアトリビュートを更新
    """
    reviews, review_contexts = parse_star_review_vote(soup)
    scraping_data.reviews = reviews 
    #print('star items', map(lambda x:x.star, reviews) )
    if hasattr(scraping_data, 'review_contexts'):
        scraping_data.review_contexts = review_contexts
    else:
        setattr(scraping_data, 'review_contexts', review_contexts)

    """
    scraping_data.reviewが空リストかNoneの場合でも処理を続行: 
    NOTE: 古いIFではNoneの場合、処理を終了していた
    """
    #print('[DEBUG] A1')
    if scraping_data.reviews == [] or scraping_data.reviews == None:
        #return
        pass
    #print('[DEBUG] A2')
    """
    全テキスト情報をトークナイズ
    """
    all_tf = tokenize_all(soup)
    if hasattr(scraping_data, 'all_tf'):
        scraping_data.all_tf = all_tf
    else:
        setattr(scraping_data, 'all_tf', all_tf)
    
 
    """
    商品説明情報を取得する
    """
    (productinfo, tf) = parse_productinfo(soup)
    if hasattr(scraping_data, 'product_info'):
        scraping_data.product_info = productinfo
    else:
        setattr(scraping_data, 'product_info', productinfo)
    if hasattr(scraping_data, 'product_info_tf'):
        scraping_data.product_info_tf = tf
    else:
        setattr(scraping_data, 'product_info_tf', tf)

    """
    調和平均を計算する
    """
    harmonic_mean = calculate_harmonic_mean(scraping_data.reviews)
    if hasattr(scraping_data, 'harmonic_mean'):
        scraping_data.harmonic_mean = harmonic_mean
    else:
        setattr(scraping_data, 'harmonic_mean', harmonic_mean)
    
    """
    単純平均を計算する
    """
    normal_mean = calculate_normal_mean(scraping_data.reviews)
    if hasattr(scraping_data, 'normal_mean'):
        scraping_data.normal_mean = normal_mean
    else:
        setattr(scraping_data, 'normal_mean', normal_mean)

    """
    contextのトークナイズを行う
    """
    review_tf    = tokenize_reviews(scraping_data.review_contexts)
    #print('review_tf ', review_tf)
    if hasattr(scraping_data, 'review_tf'):
        scraping_data.review_tf = review_tf
    else:
        setattr(scraping_data, 'review_tf', review_tf)

    """
    relevancyの計算
    """
    (rel, cnt, relevancy_term) = calc_relevancy(review_tf, tf)
    if hasattr(scraping_data, 'relevancy'):
        scraping_data.relevancy = rel
    else:
        setattr(scraping_data, 'relevancy', rel)
    if hasattr(scraping_data, 'relevancy_term'):
        scraping_data.relevancy_term = relevancy_term
    else:
        setattr(scraping_data, 'relevancy_term', relevancy_term)

    """
    cooccurrenceの代入
    """
    if hasattr(scraping_data, 'cooccurrence'):
        scraping_data.cooccurrence = cnt
    else:
        setattr(scraping_data, 'cooccurrence', cnt)

    """
    validatorをつけたのでたぶん大丈夫であるが。。。
    """
    write_each(scraping_data)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--score',   help='Evaluate kindle referenced indexed data from db')
    parser.add_argument('--dump',   help='You can dump all calculated data from MySQL.')
    parser.add_argument('--mode',   help='You can specify DB, which local or SQL.')
    args_obj = vars(parser.parse_args())

    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    is_referenced_score     = args_obj.get('score')
    is_dump                 = args_obj.get('dump')
    mode                    = args_obj.get('mode')
    
    """
    メモリ効率が悪いのでこの取得法は徐々に廃止にしていく
    NOTE: MySQLの逐次読み出しができるようになってきたので、mode=sql, mode=localを追加して、sqlでiterateする方法も採用する
    """
    #SnapshotDeal.charge_memory()
    #all_scraping_data = SnapshotDeal.SCRAPING_DATA_POOL
    if (is_dump == None or is_dump == '') and mode and mode == 'local':
        for scraping_data in SnapshotDeal.iter_all():
            parse_eval_and_update(scraping_data )
            print(scraping_data.product_info_tf)
            print(scraping_data.review_tf)
    """
    MySQLのCラッパでSeverSideでクエリを発行する
    NOTE: Ctrl+Cを発行したとしてもハングアップする
    """
    if (is_dump == None or is_dump == '') and mode and mode == 'sql':
        for keyurl, scraping_data in get_all_data_iter():
            parse_eval_and_update(scraping_data)
            #if scraping_data.review_contexts == '': 
            #    continue
            print('[INFO] all_tf, ', scraping_data.asin, ' '.join(map(lambda x:x[0], scraping_data.all_tf) ) )
            #print('review_contexts', scraping_data.review_contexts  )
            print('[INFO] review_tf, ', scraping_data.asin, ' '.join(map(lambda x:x[0], scraping_data.review_tf) ) )
            print('[INFO] product_info_tf, ', scraping_data.asin, ' '.join(map(lambda x:x[0], scraping_data.product_info_tf) ) )
            print('[INFO] relevancy, ', scraping_data.asin, scraping_data.relevancy )
            print('[INFO] normal_mean, ', scraping_data.asin, scraping_data.normal_mean )
            print('[INFO] harmonic_mean, ', scraping_data.asin, scraping_data.harmonic_mean )

    """
    PurePythonでクエリを発行する
    ClientSideで発行するので、オンメモリでクエリを保持する
    NOTE: メモリの関係でlimitが標準でついている
    """
    if (is_dump == None or is_dump == '') and mode and mode == 'sqllimit':
        for keyurl, scraping_data in initiate_data_limit_generator(1000):
            parse_eval_and_update(scraping_data)
            if scraping_data.review_contexts == '' or scraping_data.relevancy == 0.: continue
            print('[INFO] all_tf', ' '.join(map(lambda x:x[0], scraping_data.all_tf) ) )
            #print('review_contexts', scraping_data.review_contexts  )
            print('[INFO] review_tf, ', ' '.join(map(lambda x:x[0], scraping_data.review_tf) ) )
            print('[INFO] product_info_tf, ', ' '.join(map(lambda x:x[0], scraping_data.product_info_tf) ) )
            print('[INFO] relevancy, ', scraping_data.relevancy )
            print('[INFO] normal_mean, ', scraping_data.normal_mean )
            print('[INFO] harmonic_mean, ', scraping_data.harmonic_mean )

    """
    dumpモードならMySQLからすべてのデータをiterateにて処理する
    """
    if is_dump:
        for keyurl, scraping_data in get_all_data_iter():
            print(','.join(map(lambda x:str(x).replace(',', ''), \
                ['[INFO] Dump a record to mysql', __name__, scraping_data.asin, \
                scraping_data.title.encode('utf-8'), scraping_data.url.encode('utf-8'), \
                scraping_data.harmonic_mean, scraping_data.relevancy, scraping_data.cooccurrence, \
                scraping_data.normal_mean, ':'.join(map(lambda x: str(x[0]) + '|' + str(x[1]), scraping_data.product_info_tf) )  ]) ) )
            print(scraping_data.product_info_tf)
            print(scraping_data.review_tf)
