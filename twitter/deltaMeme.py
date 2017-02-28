# coding: utf-8
from __future__ import print_function
import os
import math
import sys
import glob
import re
import json
import MeCab
from collections import Counter as C
import plyvel
import pickle
db = plyvel.DB('shadow.ldb', create_if_missing=True)
m = MeCab.Tagger('-Owakati')
for gi, name in enumerate(glob.glob('out/*')):
  day = re.search('out/(.*?_.*?_.*?)_(.*?$)', name).group(1)
  who = re.search(':\d\d_(.*?$)', name).group(1)
  f = open(name,'r')
  c = json.loads(f.read())
  favs = c['favs']
  fr   = 0 #c['fr']
  txt  = c['txt']
  oneshot = {'___META_FR___':fr, "___META_ID___%s"%who:1 }
  oneshot.update(dict(C(m.parse(txt).strip().split())) )
  db.put(bytes(name.split('/')[-1], 'utf-8'), pickle.dumps(oneshot))
  if gi % 1000 == 0:
    print(gi, day, name)
    print(favs, oneshot)
    pass
