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
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *
def fprint(x): print x


# defined parameters
KINDLE_URL = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
RETRY_NUM = 10
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
SEED_EXIST = True
SEED_NO_EXIST = False
DESIRABLE_PROCESS_NUM = 1

# set default state to scrape web pages in Amazon Kindle
def initialize_parse_and_map_data_to_local_db():
    while(True):
        try:
            print 'try connecting to amazon server...' 
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', USER_AGENT)]
            html = opener.open(KINDLE_URL, timeout = 1).read()
            soup = bs4.BeautifulSoup(html)
            print 'connected to amazon server.' 
            break
        except:
            print 'cannot connect to amazon server!' 
            continue
    for i, a in enumerate(soup.find_all('a')):
        if a.has_attr('href'):
            print 'try analyising...', i, '/', len(soup.find_all('a')) 
            unquote_url = ''
            try:
            	unquote_url = urllib.unquote(a['href']).encode('raw_unicode_escape').decode('utf-8')
            except:
                unquote_url = 'None'
            raw_url     = (lambda x:'https://www.amazon.co.jp' + x if x[0] =='/' else x)(a['href'])
            description = a.string
            scraping_data = ScrapingData()
            scraping_data.normalized_url = ''
            if '=' in raw_url:
                scraping_data.normalized_url = '/'.join( filter(lambda x:not '=' in x, raw_url.split('?').pop(0).split('/') ) )
            else:
                scraping_data.normalized_url = raw_url
            if not 'www.amazon.co.jp' in scraping_data.normalized_url:
                print '[!!!]', scraping_data.normalized_url, 'amazon out of service'
                continue
            if filter(lambda x:scraping_data.normalized_url == x[0], ALL_SCRAPING_DATA ) != []:
                print '[!!!!]', 'already parsed', scraping_data.normalized_url
                fetch_obj = filter(lambda x:scraping_data.normalized_url == x[0], ALL_SCRAPING_DATA ).pop()
                print '     ->', fetch_obj[0], fetch_obj[1].normalized_url, fetch_obj[1].title, fetch_obj[1].url
                continue
            else:
                scraping_data.url = raw_url
                if not filter_is_asin(scraping_data.url):
                    print '[!!] pass, because of this url dont be seem ASIN code.', scraping_data.url
                    continue
                """ NOTE: soupの保存はシリアライズ変換時に深度エラーになって対応できない """
                _soup = None
                scraping_data.title = (lambda x: unicode( _soup.title.string ) if x != None and x.title != None else 'Untitled')(_soup)
                ALL_SCRAPING_DATA.append( (scraping_data.normalized_url, scraping_data) )
                print '[new]', scraping_data.normalized_url, description 
                pass
            #write_each(scraping_data)

def map_data_to_local_db_from_url(scraping_data):
    html = None
    if scraping_data.html == None:
        for _ in range(RETRY_NUM):
            try:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', USER_AGENT)]
                html = opener.open(scraping_data.url, timeout = 1).read()
            except:
                print 'cannot access try number is...', _, scraping_data.url
                continue
            break
        scraping_data.html = html
        """ update html """
        write_each(scraping_data)
    else:
        html = scraping_data.html
        pass

    if html == None : return []
    
    soup = bs4.BeautifulSoup(html)
    scraping_data.title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    ret_list = []
    for i, a in enumerate(soup.find_all('a')):
        """ アマゾン外のドメインの場合、全部パス """
        if a.has_attr('href') and len(a['href']) > 1 and not 'www.amazon.co.jp' in a['href']:
            continue
        if a.has_attr('href') and len(a['href']) != 0:
            _scraping_data = ScrapingData()
            fixed_url = (lambda x: 'https://www.amazon.co.jp' + x if '/' == x[0] else x)(a['href'])
            """ ASINコードっぽくない奴はパス"""
            if not filter_is_asin(fixed_url):
                continue
            """ '\n'コードを削除 ' 'を削除 """
            fixed_url = fixed_url.replace('\n','').replace(' ','')
            _scraping_data.url = fixed_url
            _scraping_data.normalized_url = '/'.join( filter( lambda x: not '=' in x, fixed_url.split('?').pop(0).split('/') ) )
            filter_len = len( filter(lambda x: _scraping_data.normalized_url == x[0], ALL_SCRAPING_DATA ) ) 
            filter_len_in_tempory_param = len( filter(lambda x: _scraping_data.normalized_url == x[0], ret_list ) ) 
            is_already_exist = (lambda x: True if x > 0 else False )(filter_len + filter_len_in_tempory_param)
            if is_already_exist == True:
                evaluatate_other_page(_scraping_data.normalized_url, ALL_SCRAPING_DATA, scraping_data.url)
                continue
            _scraping_data.url = fixed_url
            _scraping_data.title = 'Untitled'
            ret_list.append( (_scraping_data.normalized_url, _scraping_data) )
            #print 'in ', scraping_data.url, i, fixed_url, _scraping_data.normalized_url, is_already_exist
    return ret_list

def evaluatate_other_page(normalized_url, scraping_data_list, from_url):
    split_url = normalized_url.split('?').pop(0) 
    obj_in_list = filter(lambda x:split_url in x[0], scraping_data_list)
    if obj_in_list == []:
        return
    obj = obj_in_list.pop()[1]
    normalized_from_url = from_url.split('?').pop(0).split('=').pop(0)
    #referenced_objs = filter(lambda x:x.from_url == normalized_from_url, obj.evaluated)
    if not normalized_from_url in set(map(lambda x:x.from_url, obj.evaluated)) :
        referenced_obj = Referenced() 
        referenced_obj.from_url = normalized_from_url
        obj.evaluated.append( referenced_obj )
        #print '[!!!!!!]a entity will be stocked', obj, filter(lambda x:x[0] == normalized_url, scraping_data_list), map(lambda x:x.from_url, obj.evaluated)

def filter_is_asin(url):
    is_asin = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
    if is_asin[0] in ['A', 'B', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    return False

def validate_is_asin(scraping_data_list):
    #print scraping_data_list
    ret_list = []
    for url, scraping_data in scraping_data_list:
        is_asin = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
        if is_asin[0] in ['A', 'B', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            ret_list.append( (url, scraping_data) )
            print 'http://www.amazon.co.jp/dp/' + is_asin, url, scraping_data
    return ret_list

def search_flatten_threadc(conn, chunked_list):
    to_increse_list = []
    for _, (url, scraping_data) in enumerate(chunked_list):
        if scraping_data.count >= 1:
            print 'pass ',  scraping_data.url, scraping_data.count, _, '/', len(chunked_list)
            continue
        to_increse_list.extend( map_data_to_local_db_from_url(scraping_data) )
        scraping_data.count += 1
        print 'eval ', scraping_data.url, 'counter =', scraping_data.count, ' '.join( map(lambda x:str(x), [ _, '/', len(chunked_list), len(ALL_SCRAPING_DATA), mp.current_process() ]) )
        #print 'data ', to_increse_list
    conn.send(to_increse_list)
    conn.close()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def referenced_score(scraping_data_list):
    source_list = filter(lambda x:len(x[1].evaluated) != 0, sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1) )
    #source_list = sorted(scraping_data_list, key=lambda x:len(x[1].evaluated)*-1)
    for (url, scraping_data) in source_list:
        print scraping_data.url, scraping_data, map(lambda x:x.from_url, scraping_data.evaluated)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--URL', help='set default URL which to scrape at first')
    parser.add_argument('--depth', help='how number of url this program will scrape')
    parser.add_argument('--referenced_score', help='evaluate kindle referenced indexed data from db')
    args_obj = vars(parser.parse_args())
    
    depth = (lambda x:int(x) if x else 1)( args_obj.get('depth') )
    is_referenced_score = args_obj.get('referenced_score')

    global ALL_SCRAPING_DATA
    ALL_SCRAPING_DATA = []
    
    """ SEEDが存在しないならば初期化 """
    if initiate_data(ALL_SCRAPING_DATA) == SEED_NO_EXIST:
        initialize_parse_and_map_data_to_local_db()
        ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
 
    """ referenced_scoreフラグが有効なら、評価して終了 """
    if is_referenced_score:
        referenced_score(ALL_SCRAPING_DATA)
        sys.exit(0)

    """ 深度を決めて幅優先探索 """
    for i in range(depth):
        chunked_lists = [ [] ]
        if len(ALL_SCRAPING_DATA) == 0 : 
            chunked_lists = [ ALL_SCRAPING_DATA ]
        else:
            chunked_lists = chunks(ALL_SCRAPING_DATA, len(ALL_SCRAPING_DATA)/DESIRABLE_PROCESS_NUM)
        to_increse_list = []
        threads_list = []
        for i, chunked_list in enumerate(chunked_lists):
            p_conn, c_conn = mp.Pipe()
            p = mp.Process(target=search_flatten_threadc, args=(c_conn, chunked_list,))
            p.deamon = True
            threads_list.append( (p,p_conn) )
        map(lambda x:x[0].start(), threads_list)
        for x,p_conn in threads_list:
            ALL_SCRAPING_DATA.extend( p_conn.recv() )
        map(lambda x:x[0].join(), threads_list)
        ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
    
    finish_procedure(ALL_SCRAPING_DATA)

