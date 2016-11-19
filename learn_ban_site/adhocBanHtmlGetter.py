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
    for _ in range(4):
        #opener = urllib2.build_opener()
        try:
            TIME_OUT = 5.0
            print url, _
            req = urllib2.Request(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'} )
            html = urllib2.urlopen(req, timeout=TIME_OUT).read()
            pass
        except EOFError, e:
            print('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib2.URLError, e:
            print('[WARN] Cannot access url with urllib2.URLError, ', e, 'reason', e.reason, 'num', _, url, mp.current_process() )
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
        break
    if html == None:
        return None
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' ')
 
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    anchor = ' '.join([a.text for a in soup.findAll('a') ])
    urls = ''
    for a in soup.findAll('a'):
        if a.has_key('href'):
           urls += a.get('href').encode('utf-8')

    body = (lambda x:x.text if x != None else "" )(soup.find('body') )
    return title, anchor, url, body
#soup = bs4.BeautifulSoup(html)
import feedparser
import plyvel
import sys
import regex
# ポジティブIDF辞書作成モード
if '-idf' in sys.argv:
    db = plyvel.DB('posi_contents.ldb', create_if_missing=True) 
    import json
    for line in open('./posi_156657.txt').read().split('\n'):
        line = regex.sub('\s{1,}', ' ', line)
        ents = line.split(' ')
        url = ents[0].split('?').pop(0)
        if db.get(url) != None:
            continue
        flag = None
        if ents[1] == '-': 
            flag = True
        else:
            flag = False
        reses = html_adhoc_fetcher(url)
        if reses == None:
            print 'error occurred'
            db.put(url, '___error___')
            continue
        title  = reses[0]
        anchor = reses[1]
        urls   = reses[2]
        body   = reses[3]
        try:
          print flag, url, title, anchor, urls, body
          db.put(url, json.dumps( {'f':flag, 'uk':url, 't':title, 'a':anchor, 'us':urls, 'b':body} ) )
        except:
          print 'error occurred'
          db.put(url, '___error1___' )

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

