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
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *

# defined parameters
KINDLE_URL  = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
RETRY_NUM   = 10
USER_AGENT  = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
DESIRABLE_PROCESS_NUM   = 1

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
        a_s = []
        for box_div in box_divs:
            a = box_div.find('a', {'class': 'a-link-normal'} )['title']
            a_s.append(a)
        cr_votes = [] 
        for box_div in box_divs:
            cr_vote_text = box_div.find('span', {'id' : re.compile('cr-vote-*') } ).text.replace('\n', '')
            cr_votes.append( cr_vote_text )
        context_wrap_divs = soup.findAll('div', {'id': re.compile('revData-dpReviewsMostHelpfulAUI-*') } )
        print  scraping_data, url
        for a, context_wrap_div, vote in zip(a_s, context_wrap_divs, cr_votes):
            context_div = context_wrap_div.findAll('div', {'class': 'a-section'} ).pop(0)
            print ' ' + a + ' ' + context_div.text + ' ' + vote

