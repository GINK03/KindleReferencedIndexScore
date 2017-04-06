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
import plyvel
from datetime import datetime as dt
import xml.etree.ElementTree  as ET
import os.path
import random
import concurrent.futures
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
AWS = {x[0]:x[1] for x in [x.split("=") for x in filter(lambda x:x!="", open('{home}/private_configs/aws.irep.pairs'.format(home=os.environ['HOME']), 'r').read().split('\n'))]}
ACCESS_TOKEN = AWS['ACCESS_TOKEN']
SECRET_TOKEN = AWS['SECRET_TOKEN']
conn = S3Connection( ACCESS_TOKEN, SECRET_TOKEN )

def html_adhoc_fetcher(url):
  html = None
  for t in range(5):
    opener = urllib.request.build_opener()
    TIME_OUT = 1.0
    try:
      html = opener.open(str(url), timeout = TIME_OUT).read()
    except EOFError as e:
      print('[WARN] Cannot access url with EOFError, try number is...', e, t, url, mp.current_process() )
      continue
    except urllib.error.URLError as e:
      continue
    except urllib.error.HTTPError as e:
      print('[WARN] Cannot access url with urllib2.httperror, try number is...', e, t, url, mp.current_process() )
      continue
    except ssl.SSLError as e:
      print('[WARN] Cannot access url with ssl error, try number is...', e, t, url, mp.current_process() )
      continue
    except http.client.BadStatusLine as e:
      print('[WARN] Cannot access url with BadStatusLine, try number is...', e, t, url, mp.current_process() )
      continue
    except http.client.IncompleteRead as e:
      print('[WARN] Cannot access url with IncompleteRead, try number is...', e, t, url, mp.current_process() )
      continue
    except SocketError as e:
      print('[WARN] Cannot access url with SocketError, try number is...', e, t, url, mp.current_process() )
      continue
    except UnicodeEncodeError as e:
      print('[WARN] Cannot access url with UnicodeEncodeError, try number is...', e, t, url, mp.current_process() )
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

def _driver(array):
  bucket = conn.get_bucket("irep-ml-scraping")
  key_   = Key(bucket)
  time_dirname, link, contexttype = array  
  print("link", link)
  filename = link.replace('/', '_')
  if os.path.isfile('%s/%s'%(time_dirname, filename)) is True:
    return None
  tp = html_adhoc_fetcher(link)
  print(tp)
  if tp == None:
    return None
  title, contents_all_text = tp
  print(title) 
  print("contents all text ", contents_all_text)
  key_.key   = '%s_%s_%s'%(time_dirname, contexttype, filename)
  key_.set_contents_from_string(contents_all_text)

  return None

if '-c' in sys.argv:
  while True:
    tdatetime    = dt.now()
    time_dirname = "%s"%( tdatetime.strftime('%Y_%m_%d_%H') )
    #os.system('mkdir %s'%time_dirname)
    soup         = bs4.BeautifulSoup(open('./seed').read())
    xmls         = list(filter(lambda x:'.xml' in x, [a['href'] for a in soup.findAll('a', href=True)]) )
    tus          = list(map(lambda x:(x.split('/')[-2], x), xmls))
    urls_contexttype = []
    for tu in tus:
      print(tu)
      os.system('wget -O "tmp/%s_%s.html" %s'%(time_dirname, tu[0], tu[1]) )
      tree = ET.parse('tmp/%s_%s.html'%(time_dirname, tu[0]))
      contexttype = "%s_%s"%(time_dirname, tu[0])
      [urls_contexttype.append([url, contexttype]) for url in [e.text for e in tree.getiterator('link')]]
    random.shuffle(urls_contexttype)
    timedirname_urls_contexttype = [ [time_dirname, url, contexttype] for url, contexttype in urls_contexttype]
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
      executor.map(_driver, timedirname_urls_contexttype)
    #for array in timedirname_urls:
    #  _driver(array) 
if '-d' in sys.argv:
  bucket = conn.get_bucket("irep-ml-scraping")
  for key_ in bucket.list():
    print(key_.key)
    print(key_.get_contents_as_string().decode('utf-8'))
