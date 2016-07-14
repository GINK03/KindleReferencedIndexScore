# coding: utf-8
import bs4
import sys
import urllib2
import urllib
import os.path
import __future__
import argparse
import multiprocessing as mp
import threading
import datetime
import sys
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *

# defined parameters
KINDLE_URL              = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
RETRY_NUM               = 10
USER_AGENT              = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
DESIRABLE_PROCESS_NUM   = 1

class ReferencedAmountCalculator:
    @staticmethod
    def validate_is_asin(scraping_data_list):
        ret_list = []
        for url, scraping_data in scraping_data_list:
            is_asin = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
            if is_asin[0] in ['A', 'B', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                ret_list.append( (url, scraping_data) )
        return ret_list

    @staticmethod
    def referenced_score(scraping_data_list):
        source_list = filter(lambda x:len(x[1].evaluated) != 0, sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1) )
        for (url, scraping_data) in source_list:
            print scraping_data.url, scraping_data, map(lambda x:x.from_url, scraping_data.evaluated)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--score',   help='evaluate kindle referenced indexed data from db')
    args_obj = vars(parser.parse_args())
    
    is_referenced_score = args_obj.get('score')

    """ 最初にデータベースの内容すべてをオンメモリに変換 """
    """ TODO: snapshotデータベースを参照するように変更 """
    all_scraping_data = []
    if initiate_data(all_scraping_data) == SEED_NO_EXIST:
        print 'You have to scrape amazon web site first.'
        sys.exit(0)

    """ scoreフラグが有効なら、評価 """
    if is_referenced_score:
        ReferencedAmountCalculator.referenced_score(all_scraping_data)


