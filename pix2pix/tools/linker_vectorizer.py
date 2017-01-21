# coding: utf-8
from __future__ import print_function
import os
import math
import cv2
import sys
import glob
import numpy as np
import plyvel
import json
import re

if '--check' in sys.argv:
    for k, v in json.loads(open('./linker_tags.json').read()).items():
        print(k, v['vector'] )
        print(k, v['terms'] )

# キャラクタがいる絵を抜き出す方法
chars = set(filter(lambda x:x!='', open('./dataset.kancolle.dat').read().split('\n')))

TH = 7000
linkers = set()
c = 0
linker_tags = {}
#global_fix = 'kancolle.toho.fgo'
global_fix = './kancolle.toho.fgo'
os.system('cp -r ' + './' + global_fix + '/pixiv_htmls ' + './' + global_fix + '/pixiv_htmls.fuse')
for _, (k, v) in enumerate(plyvel.DB('./' + global_fix + '/pixiv_htmls.fuse')):
    k = k.decode('utf-8')
    v = v.decode('utf-8')
    if 'URL' in k: continue
    try:
      o = json.loads(v)
    except:
      continue
    if '艦これ' not in o.get('tags'):
        continue
    print("linker",  o.get('linker') )
    if isinstance(o.get('tags'), list) == True:
        context = o.get('tags')
    else:
        context = o.get('tags').split(',')

    
    if '--only-one' in sys.argv:
        if len( set(sum(list(map(lambda x:x.split('/'), \
                    map(lambda x:re.sub('(【|】)', '', re.sub('\(.*?\)', '',x)), \
                    filter(lambda x: re.search('\d',x) == None,  context))) ), [])\
                 ) & chars ) != 1:
            continue
    linkers.add(o['linker'])
    linker_tags[o['linker']] = sum(list(map(lambda x:x.split('/'), \
            map(lambda x:re.sub('(【|】)', '', re.sub('\(.*?\)', '',x)), \
            filter(lambda x: re.search('\d',x) == None,  context))) ), [])
    print( linker_tags[o['linker']] )
    print( c,  set(linker_tags[o['linker']]) & chars )
    c += 1
    if c > TH:
        print("終わり", c )
        break
#sys.exit()
#print(linker_tags[o['linker']])
from collections import Counter as C
alltags = []
for k, v in linker_tags.items():
    print(k, v)
    alltags.extend(v)

approval_set = set()
exchange_vec = [0.]*768
term_vec = {}
from copy import copy
for i, (k, v) in enumerate(sorted(C(alltags).items(), key=lambda x:x[1]*-1)[:768]):
    print(k, v)
    approval_set.add(k)
    vec = copy(exchange_vec)
    vec[i] = 1.
    term_vec[k] = vec
result = {}
for _, (k, v) in enumerate(linker_tags.items()):
    if _ % 100 == 0:
        print("iter", _ )
    base = np.array([0.]*768)
    for what in list(map( lambda x: term_vec[x], filter(lambda x: x in approval_set, v))):
        base += np.array(what)
    #print( k, list(filter(lambda x: x in approval_set, v)), base )
    linker_tags[k] = list(base)
    result[k] = { 'vector': list(base), 'terms': list(filter(lambda x:x in approval_set, v))}


open('./linker_tags.json', 'w').write(json.dumps(result))
