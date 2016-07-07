# coding: utf-8
import bs4
import sys
import urllib2
import urllib
import cPickle as pickle
import os.path
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
        self.html_raw = ''
        self.html_context = ''
        self.amazon_rating = 0
        self.reviews = []

ALL_SCRAPING_DATA = []

def initiate_data():
    if os.path.isfile('scraped_data.dat'):
        with open('scraped_data.dat', 'r') as file:
            ALL_SCRAPING_DATA = pickle.loads(file.read())
            print ALL_SCRAPING_DATA

def finish_procedure():
    with open('scraped_data.dat', 'w') as file:
        file.write( pickle.dumps(ALL_SCRAPING_DATA) )

if __name__ == '__main__':
    initiate_data()
    while(True):
        try:
            html = urllib2.urlopen(KINDLE_URL).read()
            soup = bs4.BeautifulSoup(html)
        except socket.timeout, e::
            print 'timeout!'
            continue
        except:
            print 'cannot connect to amazon'
        break

    for i, a in enumerate(soup.find_all('a')):
        if a.has_attr('href'):
            unquote_url = ''
	    try:
            	unquote_url = urllib.unquote(a['href']).encode('raw_unicode_escape').decode('utf-8')
            except:
                unquote_url = 'None'
            raw_url     = (lambda x:'https://www.amazon.co.jp' + x if x[0] =='/' else x)(a['href'])
            description = a.string
            if 'Kindle' in unquote_url:
                if filter(lambda x:raw_url == x[0], ALL_SCRAPING_DATA ) == []:
                    try:
                        scraping_data = ScrapingData()
                        scraping_data.url = raw_url
                        scraping_data.uniq_url = ''
                        if '=' in raw_url:
                            scraping_data.uniq_url = '/'.join( raw_url.split('/')[:-1] )
                        else:
                            scraping_data.uniq_url = raw_url
                        scraping_data.html_raw = urllib2.urlopen(raw_url).read()
                        ALL_SCRAPING_DATA.append( (scraping_data.uniq_url, scraping_data) )
                        print 'new', scraped_data.uniq_url, description
                    except:
                        pass

    finish_procedure()

