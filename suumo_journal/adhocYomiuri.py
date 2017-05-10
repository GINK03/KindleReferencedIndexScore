# coding: utf-8

import os
import math
import sys
import re
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.error, urllib.parse
import http.client
import ssl
import multiprocessing as mp
from socket import error as SocketError
import bs4
from threading import Thread as T
from threading import active_count as CT
import time

def html_fetcher(url):
  html = None
  for _ in range(5):
    opener = urllib.request.build_opener()
    TIME_OUT = 10.
    try:
      html = opener.open(url, timeout = TIME_OUT).read()
      break
    except Exception as e:
      print(e)
  if html == None:
    return None

  soup = bs4.BeautifulSoup(html, "html.parser")
  title = (lambda x:str(x.string) if x != None else 'Untitled')( soup.title )
  contents0_text = (lambda x:x.text if x != None else "" ) \
          ( soup.find('article') )
  links = set([a['href'] for a in soup.find_all('a', href=True)])
  return title, contents0_text, links

html = open('./yomiuri.html').read()
soup = bs4.BeautifulSoup(html, "html.parser")


def parser(link):
    if len(link) <= 2:
      return None, link
    
    if link[0]  == '/':
      link = "http://www.yomiuri.co.jp" + link
    if "yomiuri" not in link:
      print( link, "これは範囲外ドメインです" )
      return None, link
    try:
      tp = html_fetcher(link)
    except NotImplementedError as e:
      return None, link
    if tp == None:
      return None, link
    
    title, contents, ls = tp
    mtime = re.search(r"(\d\d\d\d年\d\d月\d\d日 \d\d時\d\d分)", contents)
    if mtime is not None: 
      with open("download/%s"%mtime.group(1), "w") as f:
        f.write(contents)
    print("正常に終了しました %s"%link)
    return (ls, link)

import concurrent.futures
import pickle
from multiprocessing import Process as Pr
if '-c' in sys.argv:
  try:
    links, finished = pickle.loads( open("status.pkl", "rb").read() )
    print("前回の状態から復旧します")
  except:
    finished = set()
    links    = set()
    [links.add(link) for link in set([a['href'] for a in soup.find_all('a', href=True)])]

  while links != set():
    with concurrent.futures.ProcessPoolExecutor(max_workers=256) as executor:
      for res in executor.map(parser, links):
        ls, link = res
        finished.add(link)
        if ls is not None:
          for l in ls:
            if l not in finished:
              links.add(l)
    """ linksと、finishedの保存 """
    print("メタ情報を保存しています")
    open("status.pkl", "wb").write( pickle.dumps( (links, finished) ) )
  """
  for link in links: 
    ls = parser( link ) 
    finished.add( link ) 
    if link not in finished:
      links.add(link)
  """
