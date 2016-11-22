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
    for _ in range(3):
        #opener = urllib2.build_opener()
        try:
            TIME_OUT = 2.5
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
        except ssl.CertificateError, e:
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
    urls = []
    for a in soup.find_all('a', href=True):
        urls.append( a.get('href').encode('utf-8') )

    body = (lambda x:x.text if x != None else "" )(soup.find('body') )
    return title, anchor, urls, body
#soup = bs4.BeautifulSoup(html)
import feedparser
import sys
import regex
# ポジティブIDF辞書作成モード
if '-gq' in sys.argv:
    import json
    for line in ['いずこ']:
        line = regex.sub('\s{1,}', ' ', line)
        reses = html_adhoc_fetcher('https://www.google.co.jp/search?q=test')
        title  = reses[0]
        anchor = reses[1]
        urls   = reses[2]
        body   = reses[3]
        print title
        print urls

if '-gd' in sys.argv:
    db = plyvel.DB('posi_contents.ldb')
    import json
    for k, v in db:
        print v

