# coding: utf-8

import sys
import os
import regex
import bs4
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error 
import http.client
import ssl 
import multiprocessing as mp
from socket import error as SocketError

def html_adhoc_fetcher(url, db):
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
            print(e)
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
        break
    if html == None:
        return (None, None, None, None)
 
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:str(x.string) if x != None else 'Untitled')( soup.title )
    links =  ['http://ncode.syosetu.com' + x for x in [x for x in [ a['href'] for a in soup.find_all('a',href=True) ] if x[0] == '/' and regex.search('/[0-9a-z]{1,}/\d{1,}/', x)]]
    
    links = list(set(links))
    return (html, title,  links, soup)

import plyvel
import pickle as pickle
import copy

def stemming_pair(soup):
    contents = soup.findAll('div', {'class': 'novel_view'})
    content  = ''.join( [x.text for x in contents] )
    content  = regex.sub('\s{1,}', '\n', content)
    textlist = regex.sub('\s{1,}', '\n', content ).split('\n')
    textlistd= copy.copy(textlist) 
    textlist.insert(0, 'None')
    zipped   = list(zip(textlist, textlistd ))
    zipped.pop(0)
    zipped.pop(0)
    zipped.pop()
    
    #return zipped
    return content

if __name__ == '__main__':
    db = plyvel.DB('./url_contents_pair.ldb', create_if_missing=True)
    import MeCab
    tagger = MeCab.Tagger("-Owakati")
    if '--getall' in sys.argv:
        seedurl = 'http://ncode.syosetu.com/n7975cr/1/'
        html, title, links, soup = html_adhoc_fetcher(seedurl, db) 
        print(title)
        zipped = stemming_pair(soup)
        db.put(bytes(seedurl, 'utf-8'), bytes(zipped, 'utf-8') )
        linkstack = links
        for i, link in enumerate(linkstack):
            if db.get(bytes(link, 'utf-8')) == None:
                html, title, links, soup = html_adhoc_fetcher(link, db) 
                zipped = stemming_pair(soup)
                db.put(bytes(link, 'utf-8'), bytes(zipped, 'utf-8'))
                print(str(link), 'num=', i)
                #db.put(str(link), '\n'.join([a for a in map(lambda x:x[0] + '@@@' + x[1], zipped)] ) )
                #print('\n'.join([a for a in map(lambda x:x[0] + '@@@' + x[1], zipped)] ) )
                linkstack.extend(links)
    if '--plane' in sys.argv:
      for link, text in db:
        print(text.decode('utf-8'))
