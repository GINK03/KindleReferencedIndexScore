# coding: utf-8
import os
import math
import sys
import regex
import urllib2
import httplib
import ssl
import multiprocessing as mp
from socket import error as SocketError
import bs4

def html_adhoc_fetcher(url):
    html = None
    for _ in range(5):
        #proxy_support = urllib2.ProxyHandler({'http': 'http://153.149.157.41:8086'})
        opener = urllib2.build_opener()
        TIME_OUT = 10.
        try:
            html = opener.open(str(url), timeout = TIME_OUT).read()
        except EOFError, e:
            print('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib2.URLError, e:
            #print('[WARN] cannot urlli2.urlerror', _, url)
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
    #print html
    if html == None:
        return None
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' ')
 
    #print "c"
    soup = bs4.BeautifulSoup(html, "html.parser")
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    # contents0_text = (lambda x:x.text.encode('utf-8') if x != None else "" ) \
    #        ( soup.find('div', {'class': 'ui-section-body'}) )
    contents0_text = (lambda x:x.text.encode('utf-8') if x != None else "" ) \
            ( soup.find('div', {'class': 'ArticleBody'}) )
        
    #print "c0t", soup.find('div', {'class': 'ArticleBody'})
    links = set([a['href'] for a in soup.find_all('a', href=True)])
    return title, contents0_text, links
html = open('./asahi.html').read()
soup = bs4.BeautifulSoup(html, "html.parser")
import plyvel
import sys
db = plyvel.DB('asahi.ldb', create_if_missing=True) 
#print soup.find('div', {'class' : 'CONTENTS_MAIN' } )
# クロウラーモード
def runner(_link, links):
  tp = html_adhoc_fetcher(_link)
  if tp == None:
    return
  title, contents0, ls = tp
  for l in ls:
    try:
      utf8l = str(l)
    except:
      print l
      continue
    if db.get(utf8l) == None and l not in links:
      links.add(l)
  print "パースしたよ, 残リンク数", len(links)
  contents = contents0
  db.put(str(_link), contents )
if '-c' in sys.argv:
  from threading import Thread as T
  from threading import active_count as CT
  import time
  import cPickle as P
  import random
  try:
    links = set()
    links = P.loads(open('already_parsed_asahi.pkl').read())
    print "links are recovered"
  except:
    print "links are inited"
    
  [links.add(link) for link in set([a['href'] for a in soup.find_all('a', href=True)])]
  counter = 0
  while True:
    if links != set():
      link = links.pop()
      print link
    else:
      pass
      continue
    
    #if CT() > 1000:
    #  pass
    #  continue
    if len(link) <= 2:
        continue
    if link[0]  == '/':
        link = "http://www.asahi.com" + link
    if "www.asahi.com" not in link:
        #print link, "これは範囲外ドメインです"
        continue
    #print '[[' + str(link) + ']]'
    if db.get(str(link)) != None: 
       #print link, "はすでにパース済みです"
       continue
    if db.get(str(link)) == None:
      print 'join'
      t = T(target=runner, args=(link, links, ))
      t.start()
      #runner(link, links)
      print counter, "残リンク数", len(links)
      counter += 1
      if random.random() > 0.99:
        """ 強制終了でデータが飛んだのでその対策 """
        os.system('cp already_parsed_asahi.pkl already_parsed_asahi2.pkl')
        open('already_parsed_asahi.pkl', 'w').write(P.dumps(links))
# ダンプモード
if '-d' in sys.argv:
  for url, contents in db:
    contents = contents.lower().replace('\n', '')
    if contents == '' : continue
    contents = regex.sub('　', ' ', contents)
    contents = regex.sub('\s{1,}', ' ', contents)
    contents = regex.sub('http.*?\s', '', contents)
    for r in ['１', '２', '３', '４', '５', '６', '７', '８', '９', '０' ]:
        contents = contents.replace(r, '')
    contetns = regex.sub('\s{1,}', 'num', contents)
    print contents

