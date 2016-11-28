# coding: utf-8
import os
import math
import sys
import regex
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.error, urllib.parse
import http.client
import ssl
import multiprocessing as mp
from socket import error as SocketError
import bs4

def html_adhoc_fetcher(url):
    html = None
    for _ in range(3):
        #opener = urllib2.build_opener()
        try:
            TIME_OUT = 6.0
            print(url, _)
            req = urllib.request.Request(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'} )
            #req = urllib.request.Request(url )
            html = urllib.request.urlopen(req, timeout=TIME_OUT).read()
            pass
        except EOFError as e:
            print(('[WARN] Cannot access url with EOFError, try number is...', e, _, url, mp.current_process() ))
            continue
        except urllib.error.URLError as e:
            print(('[WARN] Cannot access url with urllib2.URLError, ', e, 'reason', e.reason, 'num', _, url, mp.current_process() ))
            continue
        except urllib.error.HTTPError as e:
            print(('[WARN] Cannot access url with urllib2.httperror, try number is...', e, _, url, mp.current_process() ))
            continue
        except ssl.SSLError as e:
            print(('[WARN] Cannot access url with ssl error, try number is...', e, _, url, mp.current_process() ))
            continue
        except ssl.CertificateError as e:
            print(('[WARN] Cannot access url with ssl error, try number is...', e, _, url, mp.current_process() ))
            continue 
        except http.client.BadStatusLine as e:
            print(('[WARN] Cannot access url with BadStatusLine, try number is...', e, _, url, mp.current_process() ))
            continue
        except http.client.IncompleteRead as e:
            print(('[WARN] Cannot access url with IncompleteRead, try number is...', e, _, url, mp.current_process() ))
            continue
        except SocketError as e:
            print(('[WARN] Cannot access url with SocketError, try number is...', e, _, url, mp.current_process() ))
            continue
        except UnicodeEncodeError as e:
            print(('[WARN] Cannot access url with UnicodeEncodeError, try number is...', e, _, url, mp.current_process() ))
            continue
        break
    if html == None:
        return None
    try:
        line = regex.sub('\n', '^A^B^C', html.decode('utf-8'))
    except:
        return None
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = bytes(regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' '), 'utf-8')
    #print(html)
    #sys.exit(0)
    soup = bs4.BeautifulSoup(html)
    print(soup.title)
    try: 
        soup = bs4.BeautifulSoup(html)
    except:
        print("HTMLのパースに失敗しました")
        return None
    title = (lambda x:str(x.string) if x != None else 'Untitled')( soup.title )
    anchor = 'ダミー'
    """anchor = ' '.join([a.text for a in soup.findAll('a') ])"""
    urls = []
    for a in soup.find_all('a', href=True):
        urls.append( a.get('href') )
        #print("debug", a.get("href"))
    """ アンカータグ a-tagを削除 """
    for t in soup.findAll("a"):
        t.extract()
    # soup.renderContents()
    body = (lambda x:x.text if x != None else "" )(soup.find('body') )
    return title, anchor, urls, body
#soup = bs4.BeautifulSoup(html)
import sys
import regex
import urllib.request, urllib.parse, urllib.error
# ポジティブIDF辞書作成モード
if '-gq' in sys.argv:
    import json
    import plyvel 
    db = plyvel.DB("kancolle.ldb", create_if_missing=True, error_if_exists=False)
    nps = open('./kancolle.dat').read().split('\n')
    print(nps)
    for line in nps:
        query = line.strip()
        print(query)
        #encoded = '+'.join(map(urllib.parse.quote_plus, ['艦これ', 'かわいい', query]))
        #reses = html_adhoc_fetcher('https://www.google.co.jp/search?client=ubuntu&channel=fs&q=' + encoded + '&num=10')
        reses = html_adhoc_fetcher('https://www.bing.com/search?q=' + urllib.parse.quote_plus('艦これ かわいい ' + query) + '&count=100')
        if reses == None:
            continue
        title  = reses[0]
        anchor = reses[1]
        urls   = reses[2]
        body   = reses[3]
        urls   = filter( lambda x:'google' not in x and 'http' in x and '/' != x[0] and 'youtube' not in x and 'blogger' not in x and 'bing' not in x and 'microsoft' not in x, urls)
        for enum, url in enumerate(urls):
            keyurl = bytes(url, 'utf-8')
            if db.get(keyurl) != None:
                print(enum, line, "すでに解析済みです")
                continue
            reses2 = html_adhoc_fetcher(url)
            if reses2 == None:
                print("htmlの取得ができませんでした")
                db.put(keyurl, bytes("___error1___", 'utf-8') )
                continue
            title2  = reses2[0]
            anchor2 = reses2[1]
            urls2   = reses2[2]
            body2   = reses2[3]
            if query not in body2:
                continue
            rures   = [("\s{1,}", " "), ("\n", " "), ("\d\d\d\d.*?:\d\d:\d\d", " "), ("<.*?>", " ")]
            for s, t in rures:
                body2 = regex.sub(s, t, body2)
            body2 = body2.lower()
            print(enum, query, "scripting 完了です")
            db.put(keyurl, bytes(body2, 'utf-8') )
if '-gd' in sys.argv:
    import plyvel
    import json
    names = set(filter(lambda x:"" != x, open('./kancolle.dat').read().split('\n')))
    db = plyvel.DB('kancolle.ldb')
    results = set()
    for ind, (k, v) in enumerate(db):
        #print(k, ind, v.decode('utf-8'))
        lines = filter(lambda x:"。" in x, v.decode('utf-8').split(' '))
        for line in lines:
            if any(map(lambda x: x in line, names)):
                line = regex.sub('\d{1,}', 'number', line)
                line = line.lower()
                results.add(line)

    open('results.txt', 'w').write('\n'.join(list(results)) )
