# coding: utf-8

import json 
import math
import sys
import os

import MeCab


tagger = MeCab.Tagger('-Owakati')
alltext = open('./positive.sites.20161121.customjson').read() + '\n' + open('./negative.sites.20161121.customjson').read()
dic = {}
count = 0
for index, line in enumerate( alltext.split('\n') ):
    raw = ' '.join(line.split(' ')[1:])
    count += 1
    try:
      obj = json.loads(raw)
    except ValueError, e:
      continue 
    body = obj['b']
    body = body.encode('utf-8')
    result = tagger.parse(body)
    if result == None:
        continue
    for term in result.split(' '):
        if dic.get(term) == None:
            dic[term] = set()
            dic[term].add(index)
        else:
            dic[term].add(index)

idf = {"___DOC_NUM___": count}
term_num = {}
for term, s in dic.iteritems():
   idf[term] = math.log( float(count) / len(s) )
   term_num[term] = len(s)

print open('idf.json', 'w').write(json.dumps(idf))
print open('term_num.json', 'w').write(json.dumps(term_num))
