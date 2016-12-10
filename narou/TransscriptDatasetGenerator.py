#coding: utf-8
from __future__ import print_function
import sys
import os
import regex
import bs4
import urllib2
import urllib 
import httplib
import ssl 
import multiprocessing as mp
from socket import error as SocketError

def html_adhoc_fetcher(url, db):
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
        except ValueError, e:
            continue
        break
    if html == None:
        return (None, None, None, None)
    """
    remove extra data
    """
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' ')
 
    soup = bs4.BeautifulSoup(html, "lxml")
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    links =  filter( lambda x:('http://animetranscripts.wikispaces.com' in x and 'Japanse' in x and 'www.wikispaces.com' not in x) or ("Japanese" in x and 'page' not in x), \
                    [ a['href'] for a in soup.find_all('a',href=True) ]) 
    links = map( lambda x: x if x[0] != '/' else 'http://animetranscripts.wikispaces.com' + x, links) 
    links = list(set(links))
    return (html, title,  links, soup)

import plyvel
import cPickle as pickle
import copy

def stemming(soup):
    contents = soup.findAll('div', {'id': 'content_view'})
    content  = ''.join( map(lambda x:x.text, contents) )
    
    return content

if __name__ == '__main__':
    db = plyvel.DB('./url_contents_pair.ldb', create_if_missing=True)
    import MeCab
    import cPickle as P
    tagger = MeCab.Tagger("-Owakati")
    if '--getall' in sys.argv:
        seedurl = 'http://animetranscripts.wikispaces.com/Code+Geass%28Japanese%29%3E01.+The+Day+a+New+Demon+Was+Born'
        html, title, links, soup = html_adhoc_fetcher(seedurl, db) 
        contents = stemming(soup)
        db.put(seedurl, contents.encode('utf-8') )
        linkstack = set(links)
        if db.get('___URL___') != None:
            for link in P.loads(db.get('___URL___')):
                linkstack.add(link)
        i = 0
        while linkstack != set():
            linkstack = set(filter(lambda x:'www.wikispaces.com' not in x and 'discussion' not in x and 'print' not in x, linkstack))
            link  = linkstack.pop()
            try:
                str(link)
            except:
                continue
            if db.get(str(link)) == None:
                i += 1
                html, title, links, soup = html_adhoc_fetcher(link, db) 
                if soup == None: 
                    db.put(str(link), '___ERROR01___')
                    continue
                contents = stemming(soup)
                db.put(str(link), contents.encode('utf-8'))
                print(str(link), 'num=', i, 'sum=', len(linkstack))
                for link in links:
                  linkstack.add(link)
                db.put('___URL___', P.dumps(linkstack))
    if '--plane' in sys.argv:
        import regex
        import re
        buff = []
        for k, v in db:
            if '___' in k: continue
            for m in re.findall(r'「(.*?)」', v):
                buff.append(m)
            for m in re.findall(r':(.*?)\s', v):
                if len(m) < 20 : continue
                if len(m) > 2000: continue
                buff.append(m)
        for i in range(len(buff)-1):
            print(buff[i], "CONTSPLIT", buff[i+1],"CONTEOS")


