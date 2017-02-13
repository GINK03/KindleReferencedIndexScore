# coding: utf-8
import os
import math
import sys
import regex
import urllib.request, urllib.error, urllib.parse
import http.client
import ssl
import multiprocessing as mp
from socket import error as SocketError
import bs4

def html_adhoc_fetcher(url):
    html = None
    for _ in range(5):
        opener = urllib.request.build_opener()
        TIME_OUT = 1.0
        try:
            html = opener.open(str(url), timeout = TIME_OUT).read()
        except EOFError as e:
            print('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() )
            continue
        except urllib.error.URLError as e:
            continue
        except urllib.error.HTTPError as e:
            print('[WARN] Cannot access url with urllib2.httperror, try number is...', e, _, url, mp.current_process() )
            continue
        except ssl.SSLError as e:
            print('[WARN] Cannot access url with ssl error, try number is...', e, _, url, mp.current_process() )
            continue
        except http.client.BadStatusLine as e:
            print('[WARN] Cannot access url with BadStatusLine, try number is...', e, _, url, mp.current_process() )
            continue
        except http.client.IncompleteRead as e:
            print('[WARN] Cannot access url with IncompleteRead, try number is...', e, _, url, mp.current_process() )
            continue
        except SocketError as e:
            print('[WARN] Cannot access url with SocketError, try number is...', e, _, url, mp.current_process() )
            continue
        except UnicodeEncodeError as e:
            print('[WARN] Cannot access url with UnicodeEncodeError, try number is...', e, _, url, mp.current_process() )
            continue
    if html == None:
        return None
 
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:str(x.string) if x != None else 'Untitled')( soup.title )
    contents0 = sum([soup.findAll('p', {'class': 'ynDetailText'} ), \
                 soup.findAll('p', {'class': 'hbody'})], [] )
    if contents0 == []:
        return None
    contents_all_text = str(' '.join(map(lambda x:x.text, contents0)) )
    print( "code", soup.original_encoding )
    return title, contents_all_text
import feedparser
import plyvel
import sys
from datetime import datetime as dt
if '-c' in sys.argv:
  while True:
    try: 
      del db
    except: 
      print("no instance")
    tdatetime = dt.now()
    time = tdatetime.strftime('%Y_%m_%d_%H')
    #db = plyvel.DB('%s_yahoo_news.ldb'%time, create_if_missing=True) 
    db = plyvel.DB('%snews.ldb'%time, create_if_missing=True) 

    soup = bs4.BeautifulSoup(open('./seed').read())
    xmls = list(filter(lambda x:'.xml' in x, [a['href'] for a in soup.findAll('a', href=True)]) )
    tus = list(map(lambda x:(x.split('/')[-2], x), xmls))
    buff = []
    for tu in tus:
      print(tu)
      os.system('wget -O "tmp/%s.html" %s'%tu)
      import xml.etree.ElementTree  as ET
      tree = ET.parse('tmp/%s.html'%tu[0])
      buff.append([e.text for e in tree.getiterator('link')])
    allurl = sum(buff, [])
    print(allurl)
    # クロウラーモード
    for link in allurl:
      print("link", link)
      if db.get(bytes(link, 'utf-8')) == None:
        tp = html_adhoc_fetcher(link)
        print(tp)
        if tp == None:
          continue
        title, contents_all_text = tp
        print(title) 
        print("contents all text ", contents_all_text)
        db.put(bytes(link, 'utf-8'), bytes(contents_all_text, 'utf-8') )
# ダンプモード
if '-d' in sys.argv:
  for url, contents in db:
    print(contents)

