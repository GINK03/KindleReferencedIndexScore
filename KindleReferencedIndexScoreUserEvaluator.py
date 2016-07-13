# coding: utf-8
import bs4
import sys
import urllib2
import urllib
import os.path
import __future__
import argparse
import datetime
import re
import hashlib
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *

# defined parameters
NUMBER_PATTERN = r'[+-]?\d+(?:\.\d+)?' 
NUMBER_REGEX = re.compile(r'[+-]?\d+(?:\.\d+)?')

def ranking_logic():
    a, b = 0.5, 0.5

def validate_is_kindle(scraping_data):
    url     = scraping_data.url
    asin    = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
    """ ASINの最初の文字が、Bなら多分Kindleであろうという推定 """
    if asin[0] in ['B']:
        #print 'http://www.amazon.co.jp/dp/' + asin, url, scraping_data
        return True
    else:
        return False

def referenced_score(scraping_data_list):
    source_list = filter(lambda x:len(x[1].evaluated) != 0, sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1) )
    #source_list = sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1)
    for (url, scraping_data) in source_list:
        print scraping_data.url, scraping_data, map(lambda x:x.from_url, scraping_data.evaluated)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--score',   help='evaluate kindle referenced indexed data from db')
    args_obj = vars(parser.parse_args())
    
    is_referenced_score = args_obj.get('score')

    all_scraping_data = []
    if initiate_data(all_scraping_data) == SEED_NO_EXIST:
        print 'You have to scrape amazon web site first.'
        import sys
        sys.exit(0)

    for (url, scraping_data) in all_scraping_data:
        if not validate_is_kindle(scraping_data):
            continue
        soup = bs4.BeautifulSoup(scraping_data.html)
        box_divs = soup.findAll('div', {'id': re.compile('rev-dpReviewsMostHelpfulAUI-*') } )
        if box_divs == [] or box_divs == None : continue
        stars = []
        for box_div in box_divs:
            star = re.findall(NUMBER_REGEX,box_div.find('a', {'class': 'a-link-normal'} )['title']).pop(0)
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

        print  scraping_data, url
        '''
        評価データを更新する
        '''
        for star, context, vote in zip(stars, contexts, cr_votes):
            review = Review()
            hashes = str(hashlib.sha224(context.encode('utf-8')).hexdigest())            
            (review.star, review.context, review.vote, review.hashes) = star, context, vote, hashes
            is_exist = hashes in map(lambda x:x.hashes, scraping_data.reviews)
            print 'star rank ' + review.star + ' ' + review.context + 'votes ' + review.vote + ' hashes ' + review.hashes + ' is_exist ' + str(is_exist) 
            if is_exist: 
                continue
            scraping_data.reviews.append(review)
            write_each(scraping_data)

