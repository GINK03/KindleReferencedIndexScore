
import os
import sys
import math
import json
import codecs
idf = json.loads(open('./idf.json').read())
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
reidf = {}
for k in idf.keys():
    reidf[str(k)] = idf[k]
    pass
for line in open('./d1000.svm').read().split('\n'):
  ents = line.split(' ')
  try:
    title = ents[1]
  except:
    continue
  weighted_idf = {}
  for ent in ents[2:]:
      try:
        t = ent.split(':')[0]
        v = ent.split(':')[-1]
        v = float(v)
      except:
        continue
      weighted_idf[t] = math.log( math.e ** 2 + v ) * reidf[t]

  for i, (t, w) in enumerate(sorted(weighted_idf.items(), key=lambda x:x[1]*-1)):
      print(title, i, t, w)


