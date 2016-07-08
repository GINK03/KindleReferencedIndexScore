# coding: utf-8
import bs4
import sys
import urllib2
import urllib
import cPickle as pickle
import os.path
import anydbm
import __future__
import hashlib
# defined parameters
KINDLE_URL = 'https://www.amazon.co.jp/%E3%83%89%E3%83%AA%E3%83%95%E3%82%BF%E3%83%BC%E3%82%BA%EF%BC%88%EF%BC%91%EF%BC%89-%E3%83%A4%E3%83%B3%E3%82%B0%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%B3%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9-%E5%B9%B3%E9%87%8E%E8%80%95%E5%A4%AA-ebook/dp/B00CBEUBX4/ref=pd_sim_351_47?ie=UTF8&dpID=51YqRdk-GIL&dpSrc=sims&preST=_AC_UL160_SR114%2C160_&psc=1&refRID=QNE135S3MRAR0TDJMP9A'

class Reviews:
    def __init__(self):
        self.rate = 0
        self.context = ''
        self.good_num = 0
class Referenced:
    def __init__(self):
        self.from_url = ''
        self.evaluation_date = None
class ScrapingData:
    def __init__(self):
        self.url = 'https://'
        self.normalized_url = 'https://'
        self.date = 0
        self.title = ''
        self.description = ''
        self.html_raw = ''
        self.html_context = ''
        self.amazon_rating = 0
        self.reviews = []
        self.craw_revision = 0
        self.evaluated = []

# open db
def initiate_data():
    db = anydbm.open('objects.db', 'c')
    for k, v in db.iteritems():
        loads = pickle.loads(v)
        ALL_SCRAPING_DATA.append( (loads.normalized_url , loads) )
        print loads.normalized_url, loads, map(lambda x:x.from_url, loads.evaluated)
    db.close()
# close db
def finish_procedure():
    db = anydbm.open('objects.db', 'c')
    for normalized_url, obj in ALL_SCRAPING_DATA:
        dumps = pickle.dumps(obj)
        sha = hashlib.sha224(dumps).hexdigest()
        #print normalized_url, sha, obj
        db[sha] = dumps
    db.close()
    #with open('scraped_data.dat', 'w') as file:
    #    file.writelines( pickle.dumps(ALL_SCRAPING_DATA) )

# set default state to scrape web pages in Amazon Kindle
def get_soup_from_default_node():
    while(True):
        try:
            print 'try connecting to amazon server.' 
            html = urllib2.urlopen(KINDLE_URL).read()
            soup = bs4.BeautifulSoup(html)
            print 'connected to amazon server.' 
            return soup
        except:
            print 'cannot connect to amazon server!' 
            continue

def parse_and_map_data_to_local_db(soup):
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
            if not 'amazon.co.jp' in scraping_data.normalized_url:
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
                # NOTE: soupの保存は深度エラーになって対応できない
                _soup = None
                #try:
                #    _soup = bs4.BeautifulSoup( urllib2.urlopen( scraping_data.url ) )
                #except:
                #    print 'an error was occurred! with', scraping_data.url
                #    pass
                scraping_data.title = (lambda x: unicode( _soup.title.string ) if x != None and x.title != None else 'Untitled')(_soup)
                ALL_SCRAPING_DATA.append( (scraping_data.normalized_url, scraping_data) )
                print '[new]', scraping_data.normalized_url, description 
                pass

def map_data_to_local_db_from_url(scraping_data):
    try:
        html = urllib2.urlopen(scraping_data.url).read()
    except:
        return []
    soup = bs4.BeautifulSoup(html)
    scraping_data.title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    ret_list = []
    for i, a in enumerate(soup.find_all('a')):
        # アマゾン外のドメインの場合、全部パス
        if a.has_attr('href') and len(a['href']) > 1 and not 'www.amazon.co.jp' in a['href']:
            continue
        if a.has_attr('href') and len(a['href']) != 0:
            _scraping_data = ScrapingData()
            fixed_url = (lambda x: 'https://www.amazon.co.jp' + x if '/' == x[0] else x)(a['href'])
            # ASINコードっぽくない奴はパス
            if not filter_is_asin(fixed_url):
                continue
            _scraping_data.url = fixed_url
            _scraping_data.normalized_url = '/'.join( filter( lambda x: not '=' in x, fixed_url.split('?').pop(0).split('/') ) )
            filter_len = len( filter(lambda x: _scraping_data.normalized_url == x[0], ALL_SCRAPING_DATA ) ) 
            filter_len_in_tempory_param = len( filter(lambda x: _scraping_data.normalized_url == x[0], ret_list ) ) 
            is_already_exist = (lambda x: True if x > 0 else False )(filter_len + filter_len_in_tempory_param)
            if is_already_exist == True:
                print '[*special*] evaluate ', _scraping_data.normalized_url
                evaluatate_other_page(_scraping_data.normalized_url, ALL_SCRAPING_DATA, scraping_data.url)
                continue
            _scraping_data.url = fixed_url
            _scraping_data.title = 'Untitled'
            ret_list.append( (_scraping_data.normalized_url, _scraping_data) )
            print 'in ', scraping_data.url, i, fixed_url, _scraping_data.normalized_url, is_already_exist
    return ret_list

def evaluatate_other_page(normalized_url, scraping_data_list, from_url):
    split_url = normalized_url.split('?').pop(0) 
    obj_in_list = filter(lambda x:x[0] == split_url, scraping_data_list)
    if obj_in_list == []:
        print 'evaluate will pass,', normalized_url
        return
    obj = obj_in_list.pop()[1]
    referenced_objs = filter(lambda x:x.from_url == split_url, obj.evaluated)
    if referenced_objs == []:
        referenced_obj = Referenced() 
        referenced_obj.from_url = from_url.split('?').pop(0)
        obj.evaluated.append( referenced_obj )
    print obj, filter(lambda x:x[0] == normalized_url, scraping_data_list), obj.evaluated

def filter_is_asin(url):
    is_asin = (lambda x:x.pop() if x != [] else '?')( filter(lambda x:len(x) == 10, url.split('?').pop(0).split('/')) )
    if is_asin[0] in ['A', 'B', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
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

# ALL_SCRAPING_DATA = []
if __name__ == '__main__':
    global ALL_SCRAPING_DATA
    ALL_SCRAPING_DATA = []
    initiate_data()
    #sys.exit(0)
    soup = get_soup_from_default_node()
    parse_and_map_data_to_local_db(soup)
    ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
    
    to_increse_list = []
    for (ur, scraping_data) in ALL_SCRAPING_DATA:
        to_increse_list.extend( map_data_to_local_db_from_url(scraping_data) )
    ALL_SCRAPING_DATA.extend( to_increse_list )
    ALL_SCRAPING_DATA = validate_is_asin(ALL_SCRAPING_DATA)
    
    finish_procedure()

