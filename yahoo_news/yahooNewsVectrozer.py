# coding: utf-8

import glob
import plyvel

import os
import math
import sys

import MeCab

from collections import Counter

import pickle
import json
import re
def only_dump():
  m = MeCab.Tagger ("-Owakati")
  for dbname in glob.glob('./*.ldb'):
    date = re.search('(\d\d\d\d_\d\d_\d\d)', dbname).group(1)
    try:
      db = plyvel.DB(dbname, create_if_missing=False)
    except plyvel._plyvel.IOError as e:
      continue
    for url, context in db:
      url, context = str(url, 'utf-8'), str(context, 'utf-8')
      print(m.parse(context).strip())

def main():
  idf = json.loads(open('./words_idf.json').read())
  m = MeCab.Tagger ("-Owakati")
  date_term_freq = dict()
  words = set()
  for dbname in glob.glob('./*.ldb'):
    date = re.search('(\d\d\d\d_\d\d_\d\d)', dbname).group(1)
    # ここアドホック, 2回以上ldb読み込まない
    if date_term_freq.get(date) != None : 
      continue
    print(dbname)
    date_term_freq[date] = dict()
    try:
      db = plyvel.DB(dbname, create_if_missing=False)
    except plyvel._plyvel.IOError as e:
      continue
    for url, context in db:
      url, context = str(url, 'utf-8'), str(context, 'utf-8')
      # ここアドホック、headlineのみ
      if 'headline' not in url:
        continue
      for term, freq in Counter(m.parse(context).split()).items():
        if date_term_freq[date].get(term) == None: date_term_freq[date][term] = 0.
        date_term_freq[date][term] += freq

  date_id_freq = {}
  term_id      = {}
  for date, term_freq in date_term_freq.items():
    for term, freq in term_freq.items():
      if idf.get(term) != None:
        if term_id.get(term) == None: term_id[term] = len(term_id)
        if date_id_freq.get(date) == None: date_id_freq[date] = {}
        id = term_id.get(term)
        if date_id_freq[date].get(id) == None: 
          date_id_freq[date][id] = freq*idf[term]
        date_term_freq[date][term] = freq*idf[term]
      else:
        #print(date, "nohappend", term, freq)
        pass
  open('date_term_freq.pkl', 'wb').write(pickle.dumps(date_term_freq))
  open('id_term.pkl', 'wb').write(pickle.dumps(id_term))
  open('date_id_freq.pkl', 'wb').write(pickle.dumps(date_id_freq))
  pass

def check():
  date_term_freq = pickle.loads(open('date_term_freq.pkl', 'rb').read() )
  id_term        = pickle.loads(open('id_term.pkl', 'rb').read() )
  date_id_freq   = pickle.loads(open('date_id_freq.pkl', 'rb').read() )

  for id, term in id_term.items():
    print(id, term)


from sklearn import linear_model 
from sklearn.externals import joblib
def elasticnet():
  class KPI:
    def __init__(self):
      self.imps = 0.
      self.clks = 0.
  term_date_kpi = {}
  for rawY in filter(lambda x:x!=[], [x.split() for x in open('./sample_Y.csv').read().split('\n')] ):
    term = rawY[0]
    date = rawY[1].replace('-','_')
    imps = float(rawY[2])
    clks = float(rawY[3])
    if term_date_kpi.get(term) == None: term_date_kpi[term] = dict()
    term_date_kpi[term][date] = KPI()
    term_date_kpi[term][date].imps = imps
    term_date_kpi[term][date].clks = clks
  date_term_freq = pickle.loads(open('date_term_freq.pkl', 'rb').read() )
  id_term        = pickle.loads(open('id_term.pkl', 'rb').read() )
  date_id_freq   = pickle.loads(open('date_id_freq.pkl', 'rb').read() )
  for target_term, target_date_kpi in sorted(term_date_kpi.items(), key=lambda x:x[0]):
    Y  = []
    Xs = []
    maxlen =  max( [max(x.keys()) for x in date_id_freq.values()]  )
    for date, id_freq in date_id_freq.items():
      if target_date_kpi.get(date) is None: continue
      print(target_term, date, target_date_kpi.get(date).imps)
      Y.append( target_date_kpi.get(date).imps )
      X = [0.] * (maxlen + 1)
      for id, freq in id_freq.items():
        X[id] = freq 
      Xs.append( X )
    model = linear_model.ElasticNet()
    model.fit(Xs, Y)
    for xs in Xs:
      print(model.predict([xs]) )
  joblib.dump(model, 'elastic.pkl')
from sklearn import linear_model 
from sklearn.externals import joblib
class Drill(object):
  def __init__(self):
    self.term    = ""
    self.coef    = 0.
def elasticnetDrill():
  class KPI:
    def __init__(self):
      self.imps = 0.
      self.clks = 0.
  term_date_kpi = {}
  for rawY in filter(lambda x:x!=[], [x.split() for x in open('./sample_Y.csv').read().split('\n')] ):
    term = rawY[0]
    date = rawY[1].replace('-','_')
    imps = float(rawY[2])
    clks = float(rawY[3])
    if term_date_kpi.get(term) == None: term_date_kpi[term] = dict()
    term_date_kpi[term][date] = KPI()
    term_date_kpi[term][date].imps = imps
    term_date_kpi[term][date].clks = clks
  date_term_freq = pickle.loads(open('date_term_freq.pkl', 'rb').read() )
  term_id        = pickle.loads(open('id_term.pkl', 'rb').read() )
  id_term = { id:term for term, id in term_id.items() }
  date_id_freq   = pickle.loads(open('date_id_freq.pkl', 'rb').read() )
  keyword_drills = {}
  for keyword, target_date_kpi in sorted(term_date_kpi.items(), key=lambda x:x[0]):
    keyword_drills[keyword] = []
    for ti, term in enumerate(term_id.keys()):
      Ys = []
      Xs = []
      for date, kpi in target_date_kpi.items():
        #print(keyword, kpi, date, term, date_id_freq.get(date).get(term_id[term]) )
        if date_id_freq.get(date).get(term_id[term]) is not None:
          Ys.append(kpi.imps)
          Xs.append( [date_id_freq.get(date).get(term_id[term])] )
      model = linear_model.ElasticNet()
      #print(Ys)
      #print(Xs)
      model.fit(Xs, Ys)
      if ti%100 == 0:
        print(" %d / %d"%(ti, len(term_id)), file=sys.stderr)
        print("keyword %s term %s coef_ %04f"%(keyword, term, model.coef_) )
      drill = Drill()
      drill.term = term
      drill.coef = model.coef_
      keyword_drills[keyword].append(drill)
    #for drill in sorted(keyword_drills[keyword], key=lambda x:x.coef*-1):
    #  print("ordered", keyword, drill.term, drill.coef)
  open('keyword_drills', 'wb').write(pickle.dumps(keyword_drills))
if __name__ == '__main__':
  if '--check' in sys.argv:
    check()
  elif '--elasticnet' in sys.argv:
    elasticnet()
  elif '--drill' in sys.argv:
    elasticnetDrill()
  elif '--only_dump' in sys.argv:
    only_dump()
  else:
    main()
