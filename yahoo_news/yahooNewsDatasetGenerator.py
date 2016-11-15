# coding: utf-8
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
    if html == None:
        return (None, None, None, None)
    """
    remove extra data
    """
    line = html.replace('\n', '^A^B^C')
    line = regex.sub('<!--.*?-->', '',  line)
    line = regex.sub('<style.*?/style>', '',  line)
    html = regex.sub('<script.*?/script>', '', line ).replace('^A^B^C', ' ')
 
    soup = bs4.BeautifulSoup(html)
    title = (lambda x:unicode(x.string) if x != None else 'Untitled')( soup.title )
    links =  map( lambda x:'http://ncode.syosetu.com' + x, \
                filter(lambda x: x[0] == '/' and regex.search('/[0-9a-z]{1,}/\d{1,}/', x), \
                    [ a['href'] for a in soup.find_all('a',href=True) ]) \
             )
    
    links = list(set(links))
    return (html, title,  links, soup)

import plyvel
import cPickle as pickle
import copy

def stemming_pair(soup):
    contents = soup.findAll('div', {'class': 'novel_view'})
    content  = ''.join( map(lambda x:x.text, contents) )
    textlist = regex.sub('\s{1,}', '\n', content.encode('utf-8') ).split('\n')
    textlistd= copy.copy(textlist) 
    textlist.insert(0, 'None')
    zipped   = zip(textlist, textlistd )
    zipped.pop(0)
    zipped.pop(0)
    zipped.pop()
    return zipped

if __name__ == '__main__':
    db = plyvel.DB('./url_contents_pair.ldb', create_if_missing=True)
    import MeCab
    tagger = MeCab.Tagger("-Owakati")
    if '--getall' in sys.argv:
        seedurl = 'http://ncode.syosetu.com/n9669bk/1/'
        html, title, links, soup = html_adhoc_fetcher(seedurl, db) 
        zipped = stemming_pair(soup)
        db.put(seedurl, '\n'.join([a for a in map(lambda x:x[0] + '@@@' + x[1], zipped)] ) )
        linkstack = links
        for link in linkstack:
            if db.get(str(link)) == None:
                html, title, links, soup = html_adhoc_fetcher(link, db) 
                zipped = stemming_pair(soup)
                db.put(str(link), '\n'.join([a for a in map(lambda x:x[0] + '@@@' + x[1], zipped)] ) )
                print('\n'.join([a for a in map(lambda x:x[0] + '@@@' + x[1], zipped)] ) )
                linkstack.extend(links)
