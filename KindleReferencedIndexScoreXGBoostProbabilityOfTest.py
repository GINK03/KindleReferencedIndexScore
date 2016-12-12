# coding: utf-8
import os
import math
import sys
import MeCab
import subprocess
import json
import regex
import MeCab
if '--lstm' in sys.argv:
    t = MeCab.Tagger('-Owakati')
    ts = t.parse("こんにちは、汗が止まらないです").split(' ')
    for t in ts:
        print t

    pass

if '--makexgboost' in sys.argv:
    firsts = set(filter(lambda x:'' != x, open('./tmp/first.txt').read().replace('。', '。\n').split('\n')))
    lasts = set(filter(lambda x:'' != x, open('./tmp/last.txt').read().replace('。', '。\n').split('\n')))
    #print '\n'.join(lasts)
    diff = []
    for f in firsts:
        if f not in lasts:
            diff.append(f)
    print '\n'.join(diff)
    """
    tfidfを作成
    """
    toidf = []
    toidf.extend(lasts)
    toidf.extend(diff)
    c = 0
    idf = {}
    from collections import Counter as C
    for line in toidf:
        c += 1
        m = MeCab.Tagger('-Owakati')
        for t, f in C(m.parse(line).strip().split(' ')).items():
            if idf.get(t) == None:
                idf[t] = 1
            else:
                idf[t] += 1

    for t in idf.keys():
        idf[t] = math.log( c / idf[t] )
    it = {}
    ti = {}
    for i, (t, w) in enumerate(sorted(idf.items(), key=lambda x:x[1]*-1)):
        print i, t, w
        it[i] = t
        ti[t] = i
    import cPickle as P
    open('./tmp/differ.idf.p', 'w').write(P.dumps(idf))
    open('./tmp/differ.it.p', 'w').write(P.dumps(it))
    open('./tmp/differ.ti.p', 'w').write(P.dumps(ti))
    buff = []
    for l in lasts:
        tmp = []
        m = MeCab.Tagger('-Owakati')
        tmp.append('1')
        for t, f in C(m.parse(l).strip().split(' ')).items():
            tmp.append(':'.join(map(str, [ti[t], f*idf[t]])))
        buff.append(' '.join(tmp))
    for d in diff:
        tmp = []
        m = MeCab.Tagger('-Owakati')
        tmp.append('0')
        for t, f in C(m.parse(d).strip().split(' ')).items():
            tmp.append(':'.join(map(str, [ti[t], f*idf[t]])))
        buff.append(' '.join(tmp))
    import random
    random.shuffle(buff)
    open('./tmp/differ.train.svmfmt', 'w').write('\n'.join(buff[:len(buff)*3/4]))
    open('./tmp/differ.test.svmfmt', 'w').write('\n'.join(buff[len(buff)*3/4+1:]))
    res = subprocess.check_output(['xgboost', 'xgboost.conf'])
    print res
    res = subprocess.check_output(['mv', './0005.model', './tmp/differ.train.svmfmt', './tmp/differ.test.svmfmt', './tmp/differ.idf.p', './tmp/differ.it.p', './tmp/differ.ti.p', '/tmp'])
    res = subprocess.check_output(['cp', './tmp/first.txt', '/tmp'])
    print res



if '--xgboost' in sys.argv:
    import cPickle as P
    it = P.loads(open('/tmp/differ.it.p').read())
    ti = P.loads(open('/tmp/differ.ti.p').read())
    idf    = P.loads(open('/tmp/differ.idf.p').read())
    raws = filter(lambda x:x != '', open('./tmp/first.txt').read().split('\n'))
    wakatis = []
    rebuild = []
    for raw in raws:
        raw = raw.strip()
        m = MeCab.Tagger ("-Owakati")
        indexs = []
        wakati = []
        for t in m.parse(raw).strip().split(' '):
            wakati.append(t)
            if ti.get(t) == None:
                print 'error', t
                pass
            else:
                indexs.append( str(ti[t]) )
        wakatis.append(wakati)
        rebuild.append(' '.join(indexs))

    open('/tmp/xgboost.before.check', 'w').write('\n'.join(rebuild))

    svmfmt = []
    for indexs in rebuild:
        from collections import Counter as C
        c = C(indexs.split(' '))
        
        res = []
        for index, freq in c.items():
            term = it.get(int(index))
            score = idf.get(term) * float(freq)
            res.append( [index, score] )

        dumps = [999]
        for is_list in sorted(res, key=lambda x:x[0]):
            index, score = is_list
            dumps.append( ':'.join(map(str, is_list)) )
        svmfmt.append( ' '.join(map(str, dumps)) )

    open('/tmp/xgboost.before.check.svmfmt', 'w').write('\n'.join(svmfmt))
    res = subprocess.check_output(['xgboost', './xgboost.conf', 'task=pred', 'model_in=/tmp/0005.model'])

    preds = filter(lambda x:x!= '', open('./pred.txt').read().split('\n'))

    for p,r,w in zip(preds, raws, wakatis):
        p = float(p)
        print ''.join(map(str, [100 - int(p * 100), '%の確率で間違いです。 ', r]))
