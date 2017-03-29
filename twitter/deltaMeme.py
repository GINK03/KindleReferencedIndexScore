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
import numpy as np
from boto.s3.connection import S3Connection
from boto.s3.key import Key 
import re
db = plyvel.DB('shadow.ldb', create_if_missing=True)
m = MeCab.Tagger('-Owakati')
cha = MeCab.Tagger('-Ochasen')
def shadow():
  for gi, name in enumerate(glob.glob('out/*')):
    day = re.search('out/(.*?_.*?_.*?)_(.*?$)', name).group(1)
    who = re.search(':\d\d_(.*?$)', name).group(1)
    f = open(name,'r')
    c = json.loads(f.read())
    try:
      favs = c['favs']
      fr   = c['fr']
      txt  = c['txt']
    except:
      continue
    oneshot = {'___META_FR___':fr, "___META_ID___%s"%who:1 }
    oneshot.update(dict(C(m.parse(txt).strip().split())) )
    db.put(bytes(name.split('/')[-1], 'utf-8'), pickle.dumps(oneshot))
    if gi % 1000 == 0:
      print(gi, day, name)
      print(favs, oneshot)

def xgboost_regression():
  ## boto api
  ACCESS_TOKEN = "AKIAJHOYKCP2J4UEZXRA"
  SECRET_TOKEN = input()
  conn = S3Connection(ACCESS_TOKEN, SECRET_TOKEN )
  bucket = conn.get_bucket("irep-ml-twitter-mini")
  print( bucket.list() )
  for ki, key in enumerate(bucket.list()):
    if ki%200 == 0:
      print("iter %d"%ki)
    obj = json.loads(key.get_contents_as_string().decode('utf-8'))
    #print( re.search(r'(^...._..._..)_', key.key).group(1) )
    print(obj['favs'], m.parse(obj['txt']).strip())

def w2v_s3():
  ## boto api
  ACCESS_TOKEN = "AKIAJHOYKCP2J4UEZXRA"
  SECRET_TOKEN = input()
  conn = S3Connection(ACCESS_TOKEN, SECRET_TOKEN )
  bucket = conn.get_bucket("irep-ml-twitter-mini")
  #key_   = Key(bucket)
  for key in bucket.list():
     obj = json.loads(key.get_contents_as_string().decode('utf-8'))
     print( re.search(r'(^...._..._..)_', key.key).group(1) )
     
     print(obj['favs'], obj['txt'])

# この時のiterは停止する
def w2v():
  date_txts = {}
  for gi, name in enumerate(glob.glob('out/*')):
    day = re.search('out/(.*?_.*?_.*?)_(.*?$)', name).group(1)
    who = re.search(':\d\d_(.*?$)', name).group(1)
    f = open(name,'r')
    c = json.loads(f.read())
    try:
      favs = c['favs']
      fr   = c['fr']
      txt  = c['txt']
    except:
      continue
    if date_txts.get(day) is None: date_txts[day] = []
    date_txts[day].append( m.parse(txt).strip().replace('# ', '#') )
    if gi % 1000 == 0:
      print(gi)
  os.system('rm result/*')
  for date, txts in filter(lambda x:len(x[1]) > 100000, date_txts.items()):
    open('result/_%s_len_%d.txt'%(date, len(txts)), 'w').write( '\n'.join(txts) )
  
  for name in glob.glob('result/*.txt'):
    os.system( './fasttext skipgram -input %s -output %s.model'%(name, name.split('.')[0]) )

# 辛い
from scipy import spatial
import itertools 
def relevancy():
  term_freq = {}
  for gi, name in enumerate(glob.glob('result/*.txt')):
    day = re.search('_(.*?_.*?_.*?)_(.*?$)', name).group(1)
    for term, freq in dict(C(open(name, 'r').read().replace('\n', '').split())).items():
      if term_freq.get(term) is None: term_freq[term] = 0
      term_freq[term] += freq

  intersection = None
  for gi, name in enumerate(glob.glob('result/*.vec')):
    buff = set()
    for line in open(name, 'r').read().split('\n')[1:-1]:
       w = line.split()[0]
       buff.add(w)
    if intersection is None:
      intersection = buff
    else:
      intersection = intersection & buff 
  intersection = list(intersection)
  intersection.remove('∬')
  for i in intersection:
    #print(i)
    pass
  for term, freq in sorted(term_freq.items(), key=lambda x:x[1]*-1):
    #print(term, freq)
    pass
  day_term_vec = {}
  for gi, name in enumerate(glob.glob('result/*.vec')):
    day = re.search('_(.*?_.*?_.*?)_(.*?$)', name).group(1)
    print(day)
    data = iter(filter(lambda x:''!=x, open(name, 'r').read().split('\n')))
    for d in data:
      es = d.split()
      term = es.pop(0)
      try:
        es = np.array(list(map(float, es)))
      except:
        continue
      if day_term_vec.get(day) is None: day_term_vec[day] = {}
      day_term_vec[day][term] = es
 
  #for term, freq in sorted(term_freq.items(), key=lambda x:x[1]*-1):
  for term, freq in [('プレミアムフライデー', term_freq['プレミアムフライデー']), \
    ('ｗｗｗｗｗ', term_freq['ｗｗｗｗｗ'])]:
    if '固有名詞' not in cha.parse(term):
      continue
    if term not in intersection:
      continue
    buff = [] 
    for day, term_vec in day_term_vec.items():
      neo = list(map(lambda x:1 - spatial.distance.cosine(term_vec[x], term_vec[term]), intersection))
      buff.append( (day, neo) )
    buff = sorted(buff, key=lambda x:x[0])
    for i in range(len(buff) - 1):
      t1, t2 = buff[i], buff[i+1]
      delta = np.array(t1[1]) - np.array(t2[1])
      print("%s %s <-> %s 変化量 %03f"%(term, t1[0], t2[0], np.linalg.norm(delta) - 11.0) )

    #print(day, "ramen", list(neo))
    #term_vec['ラーメン'] 
if __name__ == '__main__':
  if '--shadow' in sys.argv:
    shadow()
  if '--test' in sys.argv:
    test()
  if '--w2v' in sys.argv:
    w2v()
  if '--w2v_s3' in sys.argv:
    w2v_s3()
  if '--xgboost_regression' in sys.argv:
    xgboost_regression()
  if '--rel' in sys.argv:
    relevancy()
