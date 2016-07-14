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
KINDLE_URL          = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
RETRY_NUM           = 10
USER_AGENT          = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
SEED_EXIST          = True
SEED_NO_EXIST       = False
DESIRABLE_PROCESS_NUM = 4 

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
                """ NOTE: soup$B$NJ]B8$O%7%j%"%i%$%:JQ49;~$K?<EY%(%i!<$K$J$C$FBP1~$G$-$J$$(B """
                _soup = None
                scraping_data.title = (lambda x: unicode( _soup.title.string ) if x != None and x.title != None else 'Untitled')(_soup)
                ALL_SCRAPING_DATA.append( (scraping_data.normalized_url, scraping_data) )
                print '[new]', scraping_data.normalized_url, description 
                pass
            #write_each(scraping_data)

def html_adhoc_fetcher(url):
    """ $BI8=`$N%"%/%;%92s?t$O(BRETRY_NUM$B$GDj5A$5$l$F$$$k(B """
    html = None
    for _ in range(RETRY_NUM):
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', USER_AGENT)]
            html = opener.open(url, timeout = 1).read()
        except:
            print 'cannot access try number is...', _, url
            continue
        break
    if html == None:
        return (None, None, None)
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    return (html, title, soup)


def map_data_to_local_db_from_url(scraping_data):
    html, soup = None, None
    if scraping_data.html == None:
        scraping_data.html, title, soup = html_adhoc_fetcher(scraping_data.url)
        """ update html """
        write_each(scraping_data)
    else:
        html, soup = scraping_data.html, bs4.BeautifulSoup(scraping_data.html)
        pass
    if html == None or html == '' : return []
    
    """ scraping_data$B$N;R%N!<%I$r(Bchild_soups$B$H$$$&JQ?tL>$GJV5Q(B, html$B$O%U%'%C%A$7$F$$$J$$$N$G7Z$$(B """
    child_scraping_data_list = []
    for i, a in enumerate(soup.find_all('a')):
        """ $B%"%^%>%s30$N%I%a%$%s$N>l9g!"A4It%Q%9(B """
        if a.has_attr('href') and len(a['href']) > 1 and not 'www.amazon.co.jp' in a['href']:
            continue
        if a.has_attr('href') and len(a['href']) != 0:
            """ $B;R%N!<%I$N:n@.(B """
            child_scraping_data = ScrapingData()
            fixed_url = (lambda x: 'https://www.amazon.co.jp' + x if '/' == x[0] else x)(a['href'])
            """ ASIN$B%3!<%I$KN`;w$7$F$$$J$$(BURL$B$O2r@O$7$J$$(B"""
            if not filter_is_asin(fixed_url):
                continue
            """ '\n'$B%3!<%I$r:o=|(B ' '$B$r:o=|(B """
            fixed_url = fixed_url.replace('\n','').replace(' ','')
            child_scraping_data.url = fixed_url
            child_scraping_data.normalized_url = '/'.join( filter( lambda x: not '=' in x, fixed_url.split('?').pop(0).split('/') ) )
            filter_len = len( filter(lambda x: child_scraping_data.normalized_url == x[0], ALL_SCRAPING_DATA ) ) 
            filter_len_in_tempory_param = len( filter(lambda x: child_scraping_data.normalized_url == x[0], child_scraping_data_list ) ) 
            is_already_exist = (lambda x: True if x > 0 else False )(filter_len + filter_len_in_tempory_param)
            if is_already_exist == True:
                evaluatate_other_page(child_scraping_data.normalized_url, ALL_SCRAPING_DATA, scraping_data.url)
                continue
            child_scraping_data.url = fixed_url
            """ $B;R%N!<%I$N(Bhtml, title$B$r<hF@(B """
            (child_scraping_data.html, child_scraping_data.title, soup ) = html_adhoc_fetcher(fixed_url)
            """ $B%G!<%?$N<hF@$K<:GT$7$F$$$?$i$=$N9T$OH4$+$9(B """
            if child_scraping_data.html == None or soup == None:
                continue
            child_scraping_data_list.append( (child_scraping_data.normalized_url, child_scraping_data) )
            write_each(child_scraping_data)
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
        child_soups = map_data_to_local_db_from_url(scraping_data)
        for child_soup in child_soups:
            write_each(child_soup)
        scraping_data.count += 1
        print 'eval ', scraping_data.url, 'counter =', scraping_data.count, ' '.join( map(lambda x:str(x), [ _, '/', len(chunked_list), len(ALL_SCRAPING_DATA), mp.current_process() ]) )
    """ pipe$B$K$h$k%G!<%?<u$1EO$7$O$?$^$K<:GT$9$k$3$H$,$"$j!"2?@i7o$H%H%i%s%6%/%7%g%s$r;+$$$?8e$KH/@8$9$k$H<h$jJV$7$,$D$+$J$$$N$G!";HMQ$7$J$$(B """
    #conn.send(to_increse_list)
    #conn.close()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--URL', help='set default URL which to scrape at first')
    parser.add_argument('--depth', help='how number of url this program will scrape')
    args_obj = vars(parser.parse_args())
    
    depth = (lambda x:int(x) if x else 1)( args_obj.get('depth') )
    is_referenced_score = args_obj.get('referenced_score')

    global ALL_SCRAPING_DATA
    ALL_SCRAPING_DATA = []
    
    """ SEED$B$,B8:_$7$J$$$J$i$P=i4|2=(B """
    if initiate_data(ALL_SCRAPING_DATA) == SEED_NO_EXIST:
        initialize_parse_and_map_data_to_local_db()
        ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
 
    """ referenced_score$B%U%i%0$,M-8z$J$i!"I>2A$7$F=*N;(B """
    if is_referenced_score:
        referenced_score(ALL_SCRAPING_DATA)
        sys.exit(0)

    """ $B?<EY$r7h$a$FI}M%@hC5:w(B """
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
        """ pipe$B$K$h$k%G!<%?<u$1EO$7$O$?$^$K<:GT$9$k$3$H$,$"$j!"2?@i7o$H%H%i%s%6%/%7%g%s$r;+$$$?8e$KH/@8$9$k$H<h$jJV$7$,$D$+$J$$$N$G!";HMQ$7$J$$(B """
        #for x,p_conn in threads_list:
        #    ALL_SCRAPING_DATA.extend( p_conn.recv() )
        map(lambda x:x[0].join(), threads_list)
        #ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
    
    #finish_procedure(ALL_SCRAPING_DATA)

