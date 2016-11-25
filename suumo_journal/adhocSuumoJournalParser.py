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
        TIME_OUT = 5
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
    #print "b"
    if html == None:
        return None
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' ')
 
    #print "c"
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    contents0_text = (lambda x:x.text.encode('utf-8') if x != None else "" )( soup.find('div', {'class': 'ui-section-body'}) )
    contents0_text = "dummy"
    links = set([a['href'] for a in soup.find_all('a', href=True)])
    return title, contents0_text, links
html = open('./index.html').read()
soup = bs4.BeautifulSoup(html)
import plyvel
import sys
db = plyvel.DB('suumo_journal.ldb', create_if_missing=True) 
# クロウラーモード
if '-c' in sys.argv:
  links = set([a['href'] for a in soup.find_all('a', href=True)])
  while links != set():
      link = links.pop()
      if "suumo.jp" not in link:
          print link, "これは範囲外ドメインです"
          continue
      if link[0]  == '/':
          link = "http://suumo.jp" + link
      #print '[[' + str(link) + ']]'
      if db.get(str(link)) != None: 
         print link, "はすでにパース済みです"
         continue
      if db.get(str(link)) == None:
        tp = html_adhoc_fetcher(link)
        if tp == None:
          continue
        title, contents0, ls = tp
        for l in ls:
            try:
                utf8l = str(l)
            except UnicodeEncodeError, e:
                continue
            if db.get(utf8l) == None and l not in links:
                links.add(l)
        print title, "パースしたよ, 残リンク数", len(links)
        contents = contents0
        db.put(str(link), contents )
# ダンプモード
if '-d' in sys.argv:
  for url, contents in db:
    print contents

