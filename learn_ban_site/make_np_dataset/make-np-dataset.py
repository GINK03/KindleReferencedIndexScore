# coding: utf-8

import json 
import math
import sys
import os

import MeCab


tagger = MeCab.Tagger('-Owakati')
positive = open('./positive.sites.20161121.customjson').read()
negative = open('./negative.sites.20161121.customjson').read()

idf = json.loads(open('./idf.json').read())

#for k, v in list(idf.iteritems())[:10]:
#    print k.encode('utf-8'), v]
urlents = set()
for index, customjson in enumerate( (positive+negative).split('\n') ):
    url = customjson.split(' ')[0]
    url = url.replace('http://', '').replace('https://', '')
    for ent in url.split('/'):
        if ent not in urlents:
            urlents.add(ent)

index_glob = 0
url_id = {}
for index, ent in enumerate( list(urlents) ):
    url_id[ent] = index
    index_glob = index

#sys.exit(0)

term_id = {}
for index, (ascii_term, v) in enumerate(idf.iteritems()):
    term_id[ascii_term] = index + index_glob + 1


for posi_nega in [(positive, 1.), (negative, 0.)]:
  for index, line in enumerate( posi_nega[0].split('\n') ):
    answer = posi_nega[1]
    uniq = line.split(' ')[0]
    raw = ' '.join( line.split(' ')[1:] )
    try:
      obj = json.loads(raw)
    except ValueError, e:
      continue 
    """ {'f':flag, 'uk':url, 't':title, 'a':anchor, 'us':urls, 'b':body} """
    body = obj['b']
    body = body.encode('utf-8')
    body_res = tagger.parse(body)
    if body_res == None:
        continue
    body_dic = {}
    for term in body_res.split(' '):
        term = term.decode('utf-8')
        index = term_id.get(term)
        if index == None:
            continue
        if body_dic.get(term) == None:
            body_dic[index+1000000]  = 0.
            body_dic[index+1000000] += (lambda x:idf[term] if idf.get(term) != None else 1. )( 0 )
        else:
            body_dic[index+1000000] += (lambda x:idf[term] if idf.get(term) != None else 1. )( 0 ) 
    
    anc = obj['a']
    anc = anc.encode('utf-8')
    anc_res = tagger.parse(anc)
    if anc_res == None:
        anc_res = ''
    anc_dic = {}
    for term in anc_res.split(' '):
        term = term.decode('utf-8')
        index = term_id.get(term)
        if index == None:
            continue
        if anc_dic.get(term) == None:
            anc_dic[index+2000000]  = 0.
            anc_dic[index+2000000] += (lambda x:idf[term] if idf.get(term) != None else 1. )( 0 )
        else:
            anc_dic[index+2000000] += (lambda x:idf[term] if idf.get(term) != None else 1. )( 0 )
            
    tit = obj['a']
    tit = tit.encode('utf-8')
    tit_res = tagger.parse(tit)
    if tit_res == None:
        tit_res = ''
    tit_dic = {}
    for term in tit_res.split(' '):
        term = term.decode('utf-8')
        index = term_id.get(term)
        if index == None:
            continue
        if tit_dic.get(term) == None:
            tit_dic[index]  = 0.
            tit_dic[index] += (lambda x:idf[term] if idf.get(term) != None else 1. )( 0 )
        else:
            tit_dic[index] += (lambda x:idf[term] if idf.get(term) != None else 1. )( 0 )
    
    uk    = obj['uk']
    us    = obj['us']
    
    key   = uk
    urldic = {}
    for ents in uniq.encode('utf-8').strip().replace('http://', '').replace('https://', '').split('/'):
        urldic[url_id.get(ents)] = 1
    """
    val   = json.dumps( \
                    [key, list(uk.encode('utf-8').strip().replace('http://', '').replace('https://', '').split('/')), \
                    tit_dic, anc_dic, body_dic] \
                    )
    """
    val = ""
    #for dic in [urldic, tit_dic, anc_dic, body_dic]:
    for dic in [urldic, tit_dic]:
      for k, v in dic.iteritems():
        val += str(k) + ":" + str(v) + " "  
    print uniq, answer, val.strip()
                    
