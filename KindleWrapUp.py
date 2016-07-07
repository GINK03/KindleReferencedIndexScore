# coding: utf-8
import bs4
import sys
import urllib2
import urllib
import cPickle as pickle
import os.path
import __future__
# defined parameters
KINDLE_URL = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'

class ScrapingData:
    class Reviews:
        def __init__(self):
            self.rate = 0
            self.context = ''
            self.good_num = 0
    def __init__(self):
        self.url = 'https://'
        self.uniq_url = 'https://'
        self.date = 0
        self.title = ''
        self.description = ''
        self.html_raw = ''
        self.html_context = ''
        self.amazon_rating = 0
        self.reviews = []

ALL_SCRAPING_DATA = []

def initiate_data():
    if os.path.isfile('scraped_data.dat'):
        with open('scraped_data.dat', 'r') as file: 
            ALL_SCRAPING_DATA = pickle.loads(file.read())
    for local in ALL_SCRAPING_DATA:
        print local
def finish_procedure():
    with open('scraped_data.dat', 'w') as file:
        file.writelines( pickle.dumps(ALL_SCRAPING_DATA) )

if __name__ == '__main__':
    initiate_data()
    while(True):
        try:
            print 'try connecting to amazon server.' 
            html = urllib2.urlopen(KINDLE_URL).read()
            soup = bs4.BeautifulSoup(html)
            print 'connected to amazon server.' 
        except:
            print 'cannot connect to amazon server!' 
            continue
        break

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
            scraping_data.uniq_url = ''
            if '=' in raw_url:
                scraping_data.uniq_url = '/'.join( raw_url.split('/')[:-1] )
            else:
                scraping_data.uniq_url = raw_url
            # - 
            if not 'amazon.co.jp' in scraping_data.uniq_url:
                print '!!!', scraping_data.uniq_url, 'amazon out of service'
                continue
            if filter(lambda x:scraping_data.uniq_url in x[0], ALL_SCRAPING_DATA ) != []:
                print '!!!!', 'already parsed', scraping_data.uniq_url
                print filter(lambda x:scraping_data.uniq_url == x[0], ALL_SCRAPING_DATA )
                continue
            else:
                #try:
                scraping_data.url = raw_url
                # soupの保存は深度エラーになって対応できない
                # scraping_data.title = (lambda x: _soup.title.string if x != None else 'None')(_soup.title)
                ALL_SCRAPING_DATA.append( (scraping_data.uniq_url, scraping_data) )
                print 'new', scraping_data.uniq_url, description 
                #except :
                pass

    finish_procedure()

