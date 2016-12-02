# coding: utf-8
from __future__ import print_function
import bs4
import sys
import urllib2
import urllib
import httplib
from socket import error as SocketError
import ssl
import os.path
import argparse
import multiprocessing as mp
#import threading as th
import datetime
from KindleReferencedIndexScoreClass import *
#from KindleReferencedIndexScoreDBs import *
#from KindleReferencedIndexScoreDBsSnapshotDealer import *
from KindleReferencedIndexScoreConfigMapper import *

SEED_EXIST          = True
SEED_NO_EXIST       = False
# set default state to scrape web pages in Amazon Kindle
def makeCookie(name, value):
    import cookielib
    return cookielib.Cookie(
        version=0, 
        name=name, 
        value=value,
        port=None, 
        port_specified=False,
        domain="kahdev.bur.st", 
        domain_specified=True, 
        domain_initial_dot=False,
        path="/", 
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )
import regex
def html_adhoc_fetcher(url):
    """ 
    標準のアクセス回数はRETRY_NUMで定義されている 
    """
    html = None
    retrys = [i for i in range(1)]
    for _ in retrys :
	import cookielib
	jar = cookielib.CookieJar()
	jar.set_cookie(makeCookie("session-token", "mu26PbfgQT4xERN6gtu8SkSoPQ7kwdgVpR7LHWqDJep5QE34DERo6AkSa0hCEhblH9k/YZkyPjnI1OIAe1+dWkZAcWZSl7fdH6SilVpQlTiFWjlsrvrvxLvb3tx2oLReL+vmG1KVWqQngeJ0JzL1asxIc+ktBPwbu7J8DPkOq05vckf90UUTPYCi6EFG2KmCYj7Yy86T9lc/CiGp7ZOUswI4cLM6rt4mKUEqnhDmpSvWKqaPWsT9EWSHXtUyyugY"))
	#ar.set_cookie(makeCookie("where", "here"))	
	headers = {"Accept-Language": "en-US,en;q=0.5","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Referer": "http://thewebsite.com","Connection": "keep-alive" } 
	request = urllib2.Request(url=url, headers=headers)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        _TIME_OUT = 5.#CM.HTTP_WAIT_SEC
        try:
            html = opener.open(request, timeout = _TIME_OUT).read()
        except EOFError, e:
            print('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib2.URLError, e:
            print('[WARN] Cannot access url with URLError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib2.HTTPError, e:
            print('[WARN] Cannot access url with urllib2.httperror, try number is...', e, _, url, mp.current_process() )
            continue
        except ssl.SSLError, e:
            print('[WARN] Cannot access url with ssl error, try number is...', e, _, url, mp.current_process() )
            continue
        except httplib.BadStatusLine, e:
            print('[WARN] Cannot access url with BadStatusLine, try number is...', e, _, url, mp.current_process() )
            continue
        except httplib.IncompleteRead, e:
            print('[WARN] Cannot access url with IncompleteRead, try number is...', e, _, url, mp.current_process() )
            continue
        except SocketError, e:
            print('[WARN] Cannot access url with SocketError, try number is...', e, _, url, mp.current_process() )
            continue
        except UnicodeEncodeError, e:
            """
            NOTE: アマゾンのサービスでは、URLに本のタイトルが日本語で記入される場合がある。これはアメリカ本国の仕様に従ったものだと思われるが、
                  ChromeやIEでは暗黙のURI変換があるためか、URLエンコードされていない。そのため、日本語が記されることが多い４番目のURLパラメータを
                  手動でURLエンコードを行って接続を確立する
            TODO: アドホック感を取り除く
            """
            urlentities     = url.split('/')
            urlentities[3]  = urllib.quote(urlentities[3].encode('utf-8'))
            rebuildurl      = '/'.join(urlentities)
            try:
                html = opener.open(str(rebuildurl), timeout = _TIME_OUT).read()
                print('[DEBUG] Access was finished correctly in exceptional URL!', _, str(rebuildurl) )
            except:
                continue
        break
    if html == None:
        return (None, None, None)
    """
    remove extra data
    """
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', '\n')
 
    soup = bs4.BeautifulSoup(html, "html.parser")
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')(soup.title )
    return (html, title, soup)

linkbuffer = list()
def map_data_to_local_db_from_url(scraping_data, uniq_hash = ''):
    ScrapingDataHelp.attribute_valid(scraping_data)
    scraping_data.last_scrape_time = time.time()

    html, soup = None, None
    if scraping_data.html == None or scraping_data.html == "":
        scraping_data.html, title, soup = html_adhoc_fetcher(scraping_data.url)
        html                            = scraping_data.html
    else:
        html, soup = scraping_data.html, bs4.BeautifulSoup(scraping_data.html)
        pass
    if html == None or html == '' : return []
    """ 
    scraping_dataの子ノードをchild_soupsという変数名で返却
    """
    child_scraping_data_list = []
    for i, a in enumerate(set(map(lambda x:x['href'], soup.find_all('a', href=True) ) ) ):
        """ 
        アマゾン外のドメインの場合、全部パス 
        """
        if not 'www.amazon.co.jp' in a:
            continue
        """ 
        子ノードの作成 
        """
        child_scraping_data = ScrapingData()
        
        fixed_url = (lambda x: 'https://www.amazon.co.jp' + x if '/' == x[0] else x)(a)
        """ 
        '\n'コードを削除 ' 'を削除 
        """
        fixed_url = fixed_url.replace('\n','').replace(' ','')
        
        """ 
        ASINコードに類似していないURLは解析しない
        this data is too fresh, no need to scrape."""
        asin = get_asin(fixed_url)
        if not asin:
            continue
        
        if asin in linkbuffer:
            print('[INFO] This asin already in linkbuffer ', asin, len(linkbuffer) )
            continue
        else:
            if len(linkbuffer) < 1000:
               linkbuffer.append(asin)
            else:
               linkbuffer.pop(0)
        child_scraping_data.asin     = asin
        child_scraping_data.title    = 'Untitled'
        
        child_scraping_data.url     = fixed_url
        
        child_scraping_data.uniq_hash = uniq_hash

        child_scraping_data.normalized_url = '/'.join( filter( lambda x: not '=' in x, fixed_url.split('?').pop(0).split('/') ) )
                   
        
       	"""
	      SQLサーバにすでにqueryが存在していて古くないのならば、処理を行わない
	      """
        if SerializedUtils.is_too_old_query(child_scraping_data) == True:
          continue
        child_scraping_data.url = fixed_url
        child_scraping_data.last_scrape_time = time.time()

        """
        scraping_dataインスタンスが持つ、html情報を元に参照しているasinのコードをアップデート
        """
        scraping_data.asins.append(asin)

        """ 
        子ノードのhtml, titleを取得 
        """
        (child_scraping_data.html, child_scraping_data.title, soup ) = html_adhoc_fetcher(fixed_url)
        
        """ 
        データの取得かHTML解析に失敗していたらその行は抜かす 
        """
        if child_scraping_data.html == None or soup == None:
            continue
        child_scraping_data_list.append((child_scraping_data.normalized_url, child_scraping_data) )
        
        write_each(child_scraping_data)
    print('[DEBUG] Finish one loop, ', scraping_data.url, scraping_data.asins)
    write_each(scraping_data)
    return []

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

def get_asin(url):
    asin = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
    if asin[0] in ['A', 'B', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return asin
    return None

def validate_is_asin(scraping_data_list):
    #print scraping_data_list
    ret_list = []
    for url, scraping_data in scraping_data_list:
        is_asin = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
        if is_asin[0] in ['A', 'B', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            ret_list.append( (url, scraping_data) )
    return ret_list

def search_flatten_multiprocess(conn, chunked_list, all_scraping_data):
    to_increse_list = []
    for _, (url, scraping_data) in enumerate(chunked_list):
        if scraping_data.count >= 1:
            continue
        child_soups = map_data_to_local_db_from_url(scraping_data)
        for (url, child_soup) in child_soups:
            if is_already_query_exist(child_soup) == False:
                write_each(child_soup)
                print(child_soup.asin)
        
        scraping_data.count += 1
        print('[DEBUG] Eval ', scraping_data.asin, scraping_data.url, 'counter =', scraping_data.count, ' '.join( map(lambda x:str(x), [ _, '/', len(chunked_list), len(all_scraping_data), mp.current_process() ]) ) )

def search_flatten_multiprocess_with_leveldb(conn):
    db = plyvel.DB('./' + SnapshotDeal.DIST_LDB_NAME, create_if_missing=True)
    for k,v in db:
      scraping_data = pickle.loads(v.replace('', '\n'))
      map_data_to_local_db_from_url(scraping_data)
      print('[DEBUG] Eval ', scraping_data.asin, scraping_data.url, 'counter =', scraping_data.count, ' '.join( map(lambda x:str(x), [ _, '/', mp.current_process() ]) ) )

def search_flatten_multiprocess_with_sql(conn, uniq_hash, index):
    for results in get_all_data_iter_box():
      """
      自分のプロセスナンバーだけ、取り出す
      """
      keyurl, scraping_data = results[index]
      if hasattr(scraping_data, 'uniq_hash') and scraping_data.uniq_hash != uniq_hash:
        scraping_data.uniq_hash = uniq_hash
        map_data_to_local_db_from_url(scraping_data, uniq_hash)
        print('[DEBUG] Eval ', scraping_data.asin, scraping_data.url, 'counter =', scraping_data.count, ' '.join( map(lambda x:str(x), [ _, '/', mp.current_process() ]) ) )
      elif not hasattr(scraping_data, 'uniq_hash'):
        setattr(scraping_data, 'uniq_hash', uniq_hash)
        map_data_to_local_db_from_url(scraping_data, uniq_hash)
        print('[DEBUG] Eval ', scraping_data.asin, scraping_data.url, 'counter =', scraping_data.count, ' '.join( map(lambda x:str(x), [ _, '/', mp.current_process() ]) ) )

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

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

import plyvel
import cPickle as pickle
import re
import json
def url_stack_control( records ):
    pass
    return set()

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--URL', help='set default URL which to scrape at first')
    parser.add_argument('--depth', help='how number of url this program will scrape')
    parser.add_argument('--mode', help='you can specify mode...')
    parser.add_argument('--refresh', help='create snapshot(true|false)')

    args_obj = vars(parser.parse_args())
  
    depth = (lambda x:int(x) if x else 10)( args_obj.get('depth') )
    
    mode = (lambda x:x if x else 'undefined')( args_obj.get('mode') )

    refresh    = (lambda x:False if x=='false' else True)( args_obj.get('refresh') )

    if mode == 'local' or mode == 'level':
      db = plyvel.DB('./tmp/asin_reviews', create_if_missing=True)
      """
      SnapshotDealデーモンが出力するデータをもとにスクレイピングを行う
      NOTE: SQLの全アクセスは非常に動作コストが高く、推奨されない
      NOTE: Snapshotが何もない場合、initialize_parse_and_map_data_to_local_dbを呼び出して初期化を行う
      """
      
      links = set([CM.REVIEW_URL])
      if db.get('___URLS___') != None:
        for link in json.loads(db.get('___URLS___')):
          if 'product-reviews' in link: continue
          if '_ntt_srch_lnk_' in link: continue
          if 'offer-listing' in link: continue
          if '/e/' in link: continue
          if '/gp/' in link: continue
          links.add(link)
        print("リカバリーしました")

      while links != set() :
          url = links.pop()
          #print('取得中です', url)
          html, title, soup = html_adhoc_fetcher(url)
          #print('取得中終わりました', url)
          if soup == None: 
              print('コンテンツが空でした', url)
              continue
          ents = soup.find_all('div', attrs={'id': re.compile('rev-dpReviewsMostHelpfulAUI-*') } )
          revs = []
          for ent in ents:
              title = ent.find('a', attrs={'class':"a-link-normal a-text-normal a-color-base"}).get('title')
              contents = regex.sub('\s{1,}', ' ', ent.text.replace('\n', '').replace(title, '') )
              revs.append( [title, contents] )
          db.put(str(url.encode('utf-8')), json.dumps(revs) )
          for i, a in enumerate(set(map(lambda x:x['href'], soup.find_all('a', href=True) ) ) ):
            if len(a) <= 2: continue
            a = (lambda x: 'https://www.amazon.co.jp' + x if '/' == x[0] else x)(a)
            if not 'www.amazon.co.jp' in a:
                continue
            if get_asin(a) == None:
                continue
            k = str(a.encode('utf-8'))
            if db.get(k) != None: continue
            if 'product-reviews' in a: continue
            if '_ntt_srch_lnk_' in a: continue
            if 'offer-listing' in a: continue
            if '/e/' in a: continue
            if '/gp/' in a: continue
            links.add(a)
            db.put('___URLS___', json.dumps(list(links)))
          print('Saved ', url, ' 残り', len(links))
    if mode == 'leveldump' or mode == 'localdump':
        db = plyvel.DB('./tmp/asin_reviews', create_if_missing=True)
        for k, raw in db:
            if k == '___URLS___': continue
            if json.loads(raw) == []: continue
            print(k)
            for txts in json.loads(raw):
                rank, con = txts
                print(rank.encode('utf-8'), con.encode('utf-8'))
