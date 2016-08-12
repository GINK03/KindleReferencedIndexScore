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
    """ 
    標準のアクセス回数はRETRY_NUMで定義されている 
    """
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
    links = filter(lambda x:'/digital/' in x , [ a['href'] for a in soup.find_all('a',href=True) ])
    reslinks = []
    for link in links:
        if 'ajax-sample-frame' in link:
            continue
        if not 'cid=' in link and not 'article=keyword' in link:
            continue
        if '?' in link:
            link = link.split('?').pop(0)

        if link[0] == '/':
            link = 'http://www.dmm.co.jp' + link
        else:
            link = link

        reent = []
        for ent in link.split('/'):
            if 'limit=' in ent or 'sort=' in ent or 'view=' in ent or regex.match('n\d=', ent):
                pass
            else:
                reent.append(ent)
        link = '/'.join(reent)
        if db.get(str(link) ):
            continue
        reslinks.append(link)

    return (html, title,  reslinks, soup)

import plyvel
import cPickle as pickle
if __name__ == '__main__':
    special_urls = '@[special_urls]'
    special_finished = '@[special_finished]'

    seedurl = 'http://www.dmm.co.jp/digital/videoa/'
    db = plyvel.DB('./dmm_url_html_store.ldb', create_if_missing=True)

    if '-d' in sys.argv:
        if db.get(special_urls):
            links_stack = pickle.loads(db.get(special_urls) )
        if db.get(special_finished):
            finished = pickle.loads(db.get(special_finished) )
        for link in links_stack:
            print('まだ', link)
        for link in finished:
            print('おわり', link)
        sys.exit(0)
    if '-da' in sys.argv:
        for k, v in db:
            if not '@[' in k:
                print(k, v)
        sys.exit(0)
    html, title, links, _ = html_adhoc_fetcher(seedurl, db)
    links_stack = set(links)
    finished    = set()
    #print(html, title, links)
    if db.get(special_urls):
        #links_stack = pickle.loads(db.get(special_urls) )
        for link in pickle.loads(db.get(special_urls) ):
            links_stack.add(link)
    if db.get(special_finished):
        finished = pickle.loads(db.get(special_finished) )
    while True:
        if links_stack == set():
            break
        link = links_stack.pop()
        finished.add(link)
        
        reent = []
        for ent in link.split('/'):
            if 'limit=' in ent or 'sort=' in ent or 'view=' in ent or regex.match('n\d=', ent):
                pass
            else:
                reent.append(ent)
        link = '/'.join(reent)
        
        if db.get(str(link)):
            print('すでにパース済みでぅ', link, len(links_stack) )
            db.put(special_urls, pickle.dumps(links_stack) )
            db.put(special_finished, pickle.dumps(finished) )
            continue
        html, title, links, soup = html_adhoc_fetcher(link, db)
        if html == None:
            continue
        if 'article=keyword' in link:
            for newlink in links:
                if not newlink in finished:
                    links_stack.add(newlink)
            db.put(special_urls, pickle.dumps(links_stack) )
            db.put(special_finished, pickle.dumps(finished) )
            pass
        for p in soup.findAll('p', {'class': 'mg-t6 tx10' }):
            p.extract()
        for dl in soup.findAll('dl', {'class': "mg-t12 mg-b0 lh3" }):
            dl.extract()
        profile = soup.findAll("div", { "class" : "mg-b20 lh4" })

        review_titles = soup.findAll('div', {'class': 'd-review__unit__title'} )
        review_many_texts = soup.findAll('div', {'class': "d-review__unit__comment fn-d-review__many-text"} )

        #for newlink in links:
        #    if newlink links_stack
        print(title, link, len(links_stack) )
        if profile != []:
            ptext = profile[0].text.encode("utf-8",'ignore')
            rtext = ''.join(map(lambda x:x.text.encode("utf-8",'ignore'), review_many_texts) )
            db.put(str(link), str(ptext+rtext))
            print(str(link), str(ptext+rtext), len(links_stack) )
        else:
            db.put(str(link), 'dummy' )
