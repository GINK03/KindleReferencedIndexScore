# coding: utf-8

import json 
import math
import sys
import os

import MeCab

mt = MeCab.Tagger("mecabrc")

res = mt.parseToNode("ハイパー雷巡コンビ")
while res != None:
    print res.surface
    print res.feature
    res = res.next


alltext = open('./positive.sites.20161121.json').read() + '\n' + open('./negative.sites.20161121.json').read()
dic = {}
for index, line in enumerate( alltext.split('\n') ):
    try:
      obj = json.loads(line)
    except ValueError, e:
      continue 
    body = obj['b']
    body = body.encode('utf-8')
    tagger = MeCab.Tagger('-Owakati')
    result = tagger.parse(body)
    if result == None:
        continue
    for term in result.split(' '):
        if dic.get(term) == None:
            dic[term] = set()
            dic[term].add(index)
        else:
            dic[term].add(index)

dicnum = {}
for term, s in dic.iteritems():
   dicnum[term] = len(s)

print open('idf.json', 'w').write(json.dumps(dicnum))
