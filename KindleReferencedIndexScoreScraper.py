# coding: utf-8
from __future__ import print_function
import bs4
import sys
import urllib2
import urllib
import ssl
import os.path
import argparse
import multiprocessing as mp
import threading
import datetime
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *
from KindleReferencedIndexScoreDBsSnapshotDealer import *
from KindleReferencedIndexScoreConfigMapper import *

SEED_EXIST          = True
SEED_NO_EXIST       = False
# set default state to scrape web pages in Amazon Kindle
def initialize_parse_and_map_data_to_local_db(all_scraping_data):
    html, title, soup = html_adhoc_fetcher(CM.KINDLE_URL)
    for i, a in enumerate(soup.find_all('a')):
        if a.has_attr('href'):
            print('[WARN] Try analyising...', i, '/', len(soup.find_all('a')) )
            unquote_url = ''
            try:
            	unquote_url = urllib.unquote(a['href']).encode('raw_unicode_escape').decode('utf-8')
            except:
                unquote_url = 'None'
            raw_url         = (lambda x:'https://www.amazon.co.jp' + x if x[0] =='/' else x)(a['href'])
            description     = a.string
            scraping_data   = ScrapingData()
                
            scraping_data.normalized_url = '/'.join( raw_url.split('?').pop(0).split('/') )
            if not 'www.amazon.co.jp' in scraping_data.normalized_url:
                continue 

            """ 
            ASINコードに類似していないURLは解析しない
            """
            asin = get_asin(scraping_data.normalized_url)
            if not asin:
                continue
            scraping_data.asin     = asin
            
            """
            scraping_dataのnormalized_urlと同一のURLを持つオブジェクトがあれば処理を中断
            ないならば、all_scraping_dataに追加して処理を再開
            """
            if filter(lambda x:scraping_data.normalized_url == x[0], all_scraping_data ) != []:
                fetch_obj = filter(lambda x:scraping_data.normalized_url == x[0], all_scraping_data ).pop()
                continue
            else:
                scraping_data.url = raw_url
                
                scraping_data.title = 'This is Seed'

                write_each(scraping_data)

                all_scraping_data.append( (scraping_data.normalized_url, scraping_data) )

def html_adhoc_fetcher(url):
    """ 
    標準のアクセス回数はRETRY_NUMで定義されている 
    """
    html = None
    for _ in range(21):
        opener = urllib2.build_opener()
        opener.addheaders.append( ('User-agent', CM.USER_AGENT) )
        opener.addheaders.append( ('Cookie', CM.SESSION_TOKEN) )
        _TIME_OUT = CM.HTTP_WAIT_SEC
        try:
            html = opener.open(str(url), timeout = _TIME_OUT).read()
        except urllib2.URLError, e:
            if _ % 10 == 0 and _ > 10:
                print('[WARN] Cannot access url with URLError, try number is...', e, _, url, mp.current_process() )
            import random
            _TIME_OUT = random.random()
            #time.sleep(random.random()/10.0)
            continue
        except urllib2.HTTPError, e:
            print('[WARN] Cannot access url with urllib2.httperror, try number is...', e, _, url, mp.current_process() )
            continue
        except ssl.SSLError, e:
            print('[WARN] Cannot access url with ssl error, try number is...', e, _, url, mp.current_process() )
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
                break
            except:
                continue
        break
    if html == None:
        return (None, None, None)
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    return (html, title, soup)


def map_data_to_local_db_from_url(scraping_data):
    html, soup = None, None
    if scraping_data.html == None or scraping_data.html == "":
        scraping_data.html, title, soup = html_adhoc_fetcher(scraping_data.url)
        html                            = scraping_data.html
        #""" add html to scraping_data.html """
        #write_each(scraping_data)
    else:
        html, soup = scraping_data.html, bs4.BeautifulSoup(scraping_data.html)
        pass
    if html == None or html == '' : return []
    """ 
    scraping_dataの子ノードをchild_soupsという変数名で返却, htmlはフェッチしていないので軽い 
    """
    child_scraping_data_list = []
    for i, a in enumerate(soup.find_all('a')):
        #print(soup.find_all('a'))
        """ 
        アマゾン外のドメインの場合、全部パス 
        """
        if not (a.has_attr('href') and len(a['href']) > 1 and not 'www.amazon.co.jp' in a['href']):
            continue
        """ 
        子ノードの作成 
        """
        child_scraping_data = ScrapingData()
        
        fixed_url = (lambda x: 'https://www.amazon.co.jp' + x if '/' == x[0] else x)(a['href'])
        """ 
        '\n'コードを削除 ' 'を削除 
        """
        fixed_url = fixed_url.replace('\n','').replace(' ','')
        
        """ 
        ASINコードに類似していないURLは解析しない
        """
        asin = get_asin(fixed_url)
        if not asin:
            continue
        child_scraping_data.asin     = asin
        child_scraping_data.title    = (lambda x:x if x else 'Untitled')(a.get('title') )
        
        child_scraping_data.url     = fixed_url
        
        child_scraping_data.normalized_url = '/'.join( filter( lambda x: not '=' in x, fixed_url.split('?').pop(0).split('/') ) )
                   
        filter_len                  = len( filter(lambda x: child_scraping_data.normalized_url == x[0], all_scraping_data ) ) 
        
        filter_len_in_tempory_param = len( filter(lambda x: child_scraping_data.normalized_url == x[0], child_scraping_data_list ) ) 
        
        is_already_exist            = (lambda x: True if x > 0 else False )(filter_len + filter_len_in_tempory_param)
        
        """
        すでに全データの中にscrape済みであるインスタンスがあれば、処理を行わない
        """
        if is_already_exist == True:
            continue

       	"""
	SQLサーバにすでにqueryが存在しているのならば、処理を行わない
	"""
	if is_already_query_exist(child_scraping_data) == True:
	   continue
 
        child_scraping_data.url = fixed_url

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
    return child_scraping_data_list

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

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--URL', help='set default URL which to scrape at first')
    parser.add_argument('--depth', help='how number of url this program will scrape')

    args_obj = vars(parser.parse_args())
  
    depth = (lambda x:int(x) if x else 1)( args_obj.get('depth') )

    #""" SEEDが存在しないならば初期化 """
    #if initiate_data(ALL_SCRAPING_DATA) == SEED_NO_EXIST:
    #    initialize_parse_and_map_data_to_local_db()
    #    ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
    
    """
    SnapshotDealデーモンが出力するデータをもとにスクレイピングを行う
    NOTE: SQLの全アクセスは非常に動作コストが高く、推奨されない
    NOTE: Snapshotが何もない場合、initialize_parse_and_map_data_to_local_dbを呼び出して初期化を行う
    """
    all_scraping_data = []
    
    _ = SnapshotDeal.get_all() 
    if _ == [] or _ == None:
        initialize_parse_and_map_data_to_local_db(all_scraping_data)
    else:
        all_scraping_data = map(lambda x:(x.url, x), SnapshotDeal.get_all() )

    """
    深さを決めて幅優先探索 
    """
    for i in range(depth):
        chunked_lists = [ [] ]
        if len(all_scraping_data) == 0 : 
            chunked_lists = [ all_scraping_data ]
        else:
            chunked_lists = chunks(all_scraping_data, len(all_scraping_data)/CM.DESIRABLE_PROCESS_NUM)
        to_increse_list = []
        threads_list = []
        for i, chunked_list in enumerate(chunked_lists):
            p_conn, c_conn = mp.Pipe()
            p = mp.Process(target=search_flatten_multiprocess, args=(c_conn, chunked_list,all_scraping_data ) )
            p.deamon = True
            threads_list.append( (p,p_conn) )
        map(lambda x:x[0].start(), threads_list)
        """ 
        pipeによるデータ受け渡しはたまに失敗することがあり、何千件とトランザクションを捌いた後に発生すると取り返しがつかないので、プロセス間通信を使用しない 
        代わりにSQLを用いてデータのやり取りを行う
        """
        #for x,p_conn in threads_list:
        #    ALL_SCRAPING_DATA.extend( p_conn.recv() )
        map(lambda x:x[0].join(), threads_list)

