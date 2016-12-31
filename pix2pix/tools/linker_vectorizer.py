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
linkers = set()
c = 1
linker_tags = {}
for k, v in plyvel.DB('./cp/pixiv_htmls'):
    k = k.decode('utf-8')
    v = v.decode('utf-8')
    if 'URL' in k: continue
    try:
     o = json.loads(v)
    except:
     continue
    c += 1
    context = ''.join(o.get('tags'))
    if '艦これ' in context or '東方' in context:
        linkers.add(o['linker'])
        linker_tags[o['linker']] = sum(list(map(lambda x:x.split('/'), map(lambda x:re.sub('\(.*?\)', '',x), filter(lambda x: re.search('\d',x) == None,  o['tags']))) ), [])
alltags = []
from collections import Counter as C
for k, v in linker_tags.items():
    #print(k, v)
    alltags.extend(v)

approval_set = set()
exchange_vec = [0.]*256
term_vec = {}
from copy import copy
for i, (k, v) in enumerate(sorted(C(alltags).items(), key=lambda x:x[1]*-1)[:256]):
    #print(k, v, allv)
    approval_set.add(k)
    vec = copy(exchange_vec)
    vec[i] = 1.
    term_vec[k] = vec
for k, v in linker_tags.items():
    base = np.array([0.]*256)
    for what in list(map( lambda x: term_vec[x], filter(lambda x: x in approval_set, v))):
        base += np.array(what)
    #print( k, v, base )
    linker_tags[k] = list(base)


open('./linker_tags.json', 'w').write(json.dumps(linker_tags))
