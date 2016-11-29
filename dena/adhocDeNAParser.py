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
        try:
            opener = urllib2.build_opener()
            TIME_OUT = 5
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36')]
            html = opener.open(url, timeout = TIME_OUT).read()
            pass
        except EOFError, e:
            print('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib2.URLError, e:
            print('[WARN] Cannot access url with urllib2.URLError, try number is...', e, _, url, mp.current_process() )
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
    contents0_text = (lambda x:x.text.encode('utf-8') if x != None else "dummy" )( soup.find('div', {'class': 'ui-main-column'}) )
    #print contents0_text
    if contents0_text == 'dummy':
        contents0_text = (lambda x:x.text.encode('utf-8') if x != None else "dummy" )( soup.find('article') )
        #print contents0_text
    links = list(set([a['href'] for a in soup.find_all('a', href=True)]) )
    #print links
    return title, contents0_text, links

def isValidURL(link, prefix):
  try:
      link = str(link)
  except UnicodeEncodeError, e:
      print link, "Unicodeエラーです"
      return False
  if len(link) < 2:
      return False
  if prefix not in link:
      #print "invalid url", link
      return False
  # この文章が入っていたら、imageなので、無視する
  if 'image' in link or '.jpg' in link or 'hatena'  in link or 'facebook' in link or 'twitter' in link or 'favorite' in link:
      return False
  if db.get(str(link)) != None: 
      #print "invalid url(db)", link
      return False
  return True

# クロウラーモード
import plyvel
import sys
db = plyvel.DB('dena.ldb', create_if_missing=True) 
if '-c' in sys.argv:
    for filename, prefix in [('./index.html-welq', 'https://welq.jp')]:#[('./index.html-iemo.jp', 'https://iemo.jp'), ('./index.html-welq', 'https://welq.jp')]:
      html = open(filename).read()
      soup = bs4.BeautifulSoup(html)
      links = set()
      for link in set([a['href'] for a in soup.find_all('a', href=True)]):
          if link[0] == '/':
              link = prefix + link 
              links.add(link)
      if db.get('___META_URLS___') != None:
          import json
          links = set(json.loads(db.get('___META_URLS___')))
          print 'URL LINKSはリカバーしました'
      while links != set():
          links = set(filter(lambda x:isValidURL(x, prefix), links) )
          if links == set(): break
          link = links.pop()
          if link[0]  == '/':
              link = prefix + link
          if isValidURL(link, prefix) == False: 
              continue 
          tp = html_adhoc_fetcher(link)
          import time 
          time.sleep(0.100)
          if tp == None:
            continue
          title, contents0, ls = tp
          for index, l in enumerate(ls):
              if len(l) > 2 and l[0] == '/':
                  ls[index] = prefix + l
          for l in ls:
            if isValidURL(l, prefix):
                links.add(l)
            else:
                pass
          print link, title, "パースしたよ, 残リンク数", len(links)
          print contents0
          contents = contents0
          db.put(str(link), contents )
          import json
          db.put('___META_URLS___', json.dumps(list(links)) )
# ダンプモード
if '-d' in sys.argv:
  for index, (url, contents) in enumerate(db):
    if 'dummy' not in contents:
        print index, regex.sub('\n', ' ', regex.sub('\s{1,}', ' ', contents) )
