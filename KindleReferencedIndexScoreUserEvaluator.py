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

NUMBER_PATTERN = r'[+-]?\d+(?:\.\d+)?' 
NUMBER_REGEX = re.compile(r'[+-]?\d+(?:\.\d+)?')


STOPWORDS = map(lambda x:x, 'abcdejghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.?:')
STOPWORDS.extend(['。', '、', 'を', 'の', 'に', 'お', 'で', 'し', 'が', 'て', 'は', 'です', 'ます'])
STOPLOGIC = (lambda x:len(x[0]) > 3 )

def ranking_logic():
    a, b = 0.5, 0.5

"""
ASINコードがキンドルのものであるかどうかを確認
"""
def validate_is_kindle(scraping_data):
    url     = scraping_data.url
    asin    = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
    """ ASINの最初の文字が、Bなら多分Kindleであろうという推定 """
    if asin[0] in ['B']:
        return True
    else:
        return False

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
    sigma       = sum( map(lambda x:x[1], hsource) )
    inverted    = sum( map(lambda x:x[1]/x[0], hsource) )
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
レビューの形態素解析を行い、tfを取得する
"""
def tokenize_reviews(reviews):
    csource     = '.'.join(map(lambda x:x.context, reviews)).encode('utf-8')
    MT= MeCab.Tagger('mecabrc')
    res = MT.parse(csource)
    items       = map(lambda x:x.split('\t').pop(0), str(res).split('\n'))
    counter     = Counter(items)
    tf          = filter(lambda x:not x[0] in STOPWORDS, sorted([(term, float(val)) for term, val in counter.items()], key=lambda x:x[1]*(-1) ) )
    tf          = filter(STOPLOGIC, tf )
    """
    ウェイトのノーマライズを行う
    """
    allwight= sum(map(lambda x:x[1], tf))
    tf          = map(lambda x:(x[0], x[1]/allwight), tf)
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
    """
    allwight= sum(map(lambda x:x[1], tf))
    tf      = map(lambda x:(x[0], x[1]/allwight), tf)
    return (productinfo.encode('utf-8'), tf)
    #print( productinfo )
    #for term, val in sorted([(term, val) for term, val in counter.items()], key=lambda x:x[1]*(-1) ) :
    #    print(term,val)

"""
星・レビューコンテキスト・vote数を取得し
Reviewのインスタンスreviewsを返却
"""
def parse_star_review_vote(soup):
    box_divs = soup.findAll('div', {'id': re.compile('rev-dpReviewsMostHelpfulAUI-*') } )
    
    if box_divs == [] or box_divs == None : 
        return []
    
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
        review = Review()
        hashes = str(hashlib.sha224(context.encode('utf-8')).hexdigest())            
        (review.star, review.context, review.vote, review.hashes) = star, context, vote, hashes
        is_exist = hashes in map(lambda x:x.hashes, scraping_data.reviews)
        #print('star rank ' + review.star + ' ' + review.context + 'votes ' + review.vote + ' hashes ' + review.hashes + ' is_exist ' + str(is_exist)  )
        if is_exist: 
            continue
        reviews.append(review)
    return reviews

"""
relevancyの計算
"""
def calc_relevancy(sourcetf, targettf, top=None):
    relevancy = 0.
    count = 0
    for tf in sourcetf:
        res = (lambda x:x.pop() if x != [] else None)( filter(lambda x:tf[0] == x[0], targettf) )
        if res == [] or res == None: continue
        relevancy += res[1] * tf[1]
        count += 1
        #if top and top < cnt : break
    return (relevancy, count )

def parse_eval_and_update(scraping_data):

    if not validate_is_kindle(scraping_data):
        return
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
    reviews = parse_star_review_vote(soup)
    scraping_data.reviews = reviews 
    """
    scraping_data.reviewが空リストかNoneの場合、処理を終了
    """
    if scraping_data.reviews == [] or scraping_data.reviews == None:
        return
    
    """
    商品説明情報を取得する
    """
    (productinfo, tf) = parse_productinfo(soup)
    if hasattr(scraping_data, 'product_info'):
        scraping_data.product_info = productinfo
    else:
        setattr(scraping_data, 'product_info', productinfo)
    if hasattr(scraping_data, 'product_info_tf'):
        scraping_data.product_info = tf
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
    review_tf    = tokenize_reviews(scraping_data.reviews)
    if hasattr(scraping_data, 'review_tf'):
        scraping_data.review_tf = review_tf
    else:
        setattr(scraping_data, 'review_tf', review_tf)

    """
    relevancyの計算
    """
    (rel, cnt ) = calc_relevancy(review_tf, tf)
    if hasattr(scraping_data, 'relevancy'):
        scraping_data.relevancy = rel
    else:
        setattr(scraping_data, 'relevancy', rel)

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
    parser.add_argument('--score',   help='evaluate kindle referenced indexed data from db')
    args_obj = vars(parser.parse_args())

    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    is_referenced_score = args_obj.get('score')

    all_scraping_data = SnapshotDeal.SCRAPING_DATA_POOL

    for scraping_data in all_scraping_data:
        parse_eval_and_update(scraping_data )
