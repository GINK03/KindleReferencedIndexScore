
from __future__ import print_function
import os
import math
import sys
import MeCab

if '--poi' in sys.argv:
    results = set()
    for line in sys.stdin:
        line = line.strip()
        if line == '' or 'Ad' in line or 'Total' in line: continue
        tp = line.split(',')
        try:
          tp.pop()
          tp.pop()
        except:
          pass
        results.add(' '.join(filter(lambda x:x!=' --' and x!='', tp)))
    for result in results:
        print(result)
if '--poipoi' in sys.argv:
    for line in sys.stdin:
        line = line.strip()
        if line == '': continue
        print(line + " <EOS>")

if '-idfgen' in sys.argv:
    m = MeCab.Tagger ("-Owakati")
    idf = {}
    c = 0

    for line in sys.stdin:
        line = line.strip()
        if line == '':continue
        if 'AD_PERFORMANCE_REPORT' in line or \
                'Ad,Headline' in line or \
                'Ad name' in line or \
                '.jpg' in line or \
                '--' in line:
                    continue
        c += 1
        tp = line.split(',')

        imps = float(tp.pop())
        clks = float(tp.pop())

        sentence = ' '.join(tp).replace(',', '')
        ts = m.parse(sentence).strip().split(' ')
        for t in set(ts):
            if idf.get(t) == None:
                idf[t] = 1
            else:
                idf[t] += 1

    import cPickle as P
    for t in idf.keys():
        idf[t] = math.log(c/ float(idf[t]) )


    it = {}
    ti = {}
    for e, t in enumerate(idf.keys()):
        it[e] = t
        ti[t] = e
        
    open('idf.p', "w").write(P.dumps(idf))
    open('it.p', "w").write(P.dumps(it))
    open('ti.p', "w").write(P.dumps(ti))

    for t, w in sorted(idf.items(), key=lambda x:x[1]*-1):
        print(t,w, ti[t])

if '--shimakaze' in sys.argv:
    imps_all = 0
    clks_all = 0
    for line in sys.stdin:
        line = line.strip()
        if 'AD_PERFORMANCE_REPORT' in line or \
                'Ad,Headline' in line or \
                'Ad name' in line or \
                '.jpg' in line or \
                '--' in line:
                    continue
        tp = line.split(',')

        imps = float(tp.pop())
        clks = float(tp.pop())
        imps_all += imps
        clks_all += clks

    print("です", 'imps_all', imps_all, 'clks_all', clks_all)
 
if '--tokitsukaze' in sys.argv:
    import cPickle as P
    from collections import Counter as C 
    idf = P.loads(open('idf.p').read() )
    it  = P.loads(open('it.p').read() )
    ti  = P.loads(open('ti.p').read() )
    m = MeCab.Tagger ("-Owakati")
    for line in sys.stdin:
        line = line.strip()
        if 'AD_PERFORMANCE_REPORT' in line or \
                'Ad,Headline' in line or \
                'Ad name' in line or \
                '.jpg' in line or \
                '--' in line:
                    continue
        tp = line.split(',')

        imps = float(tp.pop())
        clks = float(tp.pop())

        sentence = ' '.join(tp).replace(',', '')
        ts = m.parse(sentence).strip().split(' ')
        tf = C(ts)
        output = []
        for t,f in tf.items():
          output.append( ':'.join(map(str, [ti[t], idf[t]*f])) )
        output_txt = " ".join(sorted(output, key=lambda x:int(x.split(':')[0])))
        if imps <= 5. or clks <= 5 or clks/imps >= 1.0 or clks/imps == 0.: continue
        print(clks/imps, output_txt)

if '--yukikaze' in sys.argv:
    import cPickle as P
    from collections import Counter as C 
    it  = P.loads(open('it.p').read() )
    tw = {}
    for e, line in enumerate(open('./yukikaze.20161208.shuf.svm.train.model').read().split('\n')):
        line = line.strip()
        if line == "" : continue
        if e < 6: continue
        i = e - 6 + 1
        tw[it[i]] = float(line)

    for t, w in sorted(tw.items(), key=lambda x:x[1]):
        print(t,w)

            

        
