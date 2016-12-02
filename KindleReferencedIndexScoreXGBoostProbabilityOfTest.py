# coding: utf-8
import os
import math
import sys
import MeCab
import subprocess
import json
import regex
itfile = json.loads(open('./tmp/differs20161202.it.json').read())
tifile = json.loads(open('./tmp/differs20161202.ti.json').read())
idf    = json.loads(open('./tmp/differs20161202.idf.json').read())
raws = filter(lambda x:x != '', open('../differ/before_fix.txt').read().split('\n'))
wakatis = []
rebuild = []
for raw in raws:
    raw = raw.strip()
    raw = raw.lower()
    m = MeCab.Tagger ("-Owakati")
    indexs = []
    for k in tifile.keys():
        pass
    wakati = []
    for t in m.parse(raw).strip().split(' '):
        wakati.append(t)
        if tifile.get(t.decode('utf-8')) == None:
            print 'error', t
            pass
        else:
            indexs.append( str(tifile[t.decode('utf-8')]) )
    wakatis.append(wakati)
    rebuild.append(' '.join(indexs))

open('/tmp/xgboost.before.check', 'w').write('\n'.join(rebuild))

svmfmt = []
for indexs in rebuild:
    from collections import Counter as C
    c = C(indexs.split(' '))
    
    res = []
    for index, freq in c.items():
        term = itfile.get(index.decode('utf-8'))
        score = idf.get(term) * float(freq)
        res.append( [index, score] )

    dumps = [999]
    for is_list in sorted(res, key=lambda x:x[0]):
        index, score = is_list
        dumps.append( ':'.join(map(str, is_list)) )
    svmfmt.append( ' '.join(map(str, dumps)) )

open('/tmp/xgboost.before.check.svmfmt', 'w').write('\n'.join(svmfmt))

res = subprocess.check_output(['xgboost', '/etc/t.conf', 'task=pred', 'model_in=/tmp/0100.model'])

preds = filter(lambda x:x!= '', open('./pred.txt').read().split('\n'))


tw = {}
for i, w in enumerate(filter(lambda x:x!='', open('/tmp/train.txt.model').read().split('\n'))[6:]):
    i = i + 1
    t = itfile.get(str(i).decode('utf-8'))
    t = t.encode('utf-8')
    tw[t] = float(w)

for p,r,w in zip(preds, raws, wakatis):
    p = float(p)
    tp = []
    for aw in w:
        if tw.get(aw) != None:
            tp.append( (aw, str(tw[aw])) )
    tp.pop()
    tgts = sorted(tp, key=lambda x:float(x[1]))[0:3]
    tmp = ' '.join([x[0] + ':' + x[1] for x in tgts])
    
    print ''.join(map(str, [100 - int(p * 100), '%の確率で間違いです。 ', r, ' [', tmp, '] ']))
