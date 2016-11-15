# coding: utf-8
import os
import math
import sys
import regex
import urllib2
import urllib2
import httplib
import ssl
import multiprocessing as mp
from socket import error as SocketError
import bs4

def html_adhoc_fetcher(url):
    html = None
    for _ in range(5):
        opener = urllib2.build_opener()
        TIME_OUT = 1.0
        try:
            html = opener.open(str(url), timeout = TIME_OUT).read()
        except EOFError, e:
            print('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib2.URLError, e:
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
            print('[WARN] Cannot access url with UnicodeEncodeError, try number is...', e, _, url, mp.current_process() )
            continue
    if html == None:
        return None
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' ')
 
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    contents0 = soup.findAll('p', {'class': 'ynDetailText'} )
    if contents0 == []:
        return None
    contents0_text = contents0.pop().text
    return title, contents0_text
html = open('./seed.html').read()
soup = bs4.BeautifulSoup(html)
links = set()
import feedparser
import plyvel
import sys
db = plyvel.DB('yahoo_news.ldb', create_if_missing=True) 
# クロウラーモード
if '-c' in sys.argv:
  for link in set([a['href'] for a in soup.find_all('a', href=True)]):
    obj = feedparser.parse(link)
    for i, e in enumerate(obj.entries):
      print '[[' + str(i) + ']]'
      print e.title.encode('utf-8')
      print e.link
      link = str(e.link)
      if db.get(link) == None:
        tp = html_adhoc_fetcher(e.link)
        if tp == None:
          continue
        title, contents0_text = tp
        print "パースしますよ！"
        print title 
        contents = str(contents0_text.encode('utf-8'))
        print contents
        print "raw", contents0_text
        db.put(link, contents )
# ダンプモード
if '-d' in sys.argv:
  for url, contents in db:
    print contents

