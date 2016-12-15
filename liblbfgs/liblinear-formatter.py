
from __future__ import print_function
import os
import math
import sys
import MeCab
import cPickle as P
# 原初の五
# fubuki:  keywordフォーマットを処理
# Keyword,Ad group ID,Ad group,Network,Network (with search partners),Day of week,Avg. CPC,Conversions,Clicks,Impressions
if '--fubuki' in sys.argv:
    for line in sys.stdin:
        line = line.strip()
        if line == '':continue
        if 'KEYWORDS_PERFORMANCE_REPORT' in line or \
                'Keyword,Ad' in line or \
                'Ad name' in line or \
                'Total, --, --, --, --, --,' in line:
                    continue
        import re
        if re.findall('".*?"', line) != []:
            src = re.findall('".*?"', line)[-1]
            tgt = src.replace(',', '').replace('"','')
            rep = line.replace(src, tgt)
            line = rep
        tp = line.split(',')
        line = line.strip()
        imps = float(tp.pop()) # 1 impresson
        clks = float(tp.pop()) # 2 click
        cnvs = float(tp.pop()) # 3 convs
        acpc = float(tp.pop()) # 4 ave_cpc
        week = '___WEEK___' + tp.pop()        # 5 week
        nw2  = tp.pop()        # 6
        nw1  = tp.pop()
        network = '___NETWORK___' + nw1.replace(' ','') + nw2.replace(' ', '')
        adgroup_name = '___ADGROUP_NAME___' + tp.pop().replace(' ', '')
        adgroup = '___ADGROUP___' + str(int(tp.pop()))
        keywords = map(lambda x: '___KEYWORD___' + x, tp.pop().split(' ') )
        if imps <= 5. or clks <= 3 or clks/imps >= 1.0 or clks/imps == 0.: continue
        ts = []
        ts.append(week)
        ts.append(network)
        ts.append(adgroup_name)
        ts.append(adgroup)
        for keyword in keywords:
            ts.append(keyword)
        print( clks/imps, ','.join(ts))
    sys.exit()

# 原初の五
# sazanami:  ageフォーマットを処理
# Age Range,Ad group ID,Ad group,Network,Network (with search partners),Day of week,Avg. CPC,Conversions,Clicks,Impressions
if '--sazanami' in sys.argv:
    for line in sys.stdin:
        line = line.strip()
        if line == '':continue
        if 'AGE_RANGE_PERFORMANCE_REPORT' in line or \
                'Age Range,Ad' in line or \
                'Total, --, --, --, --, --,' in line:
                    continue
        import re
        if re.findall('".*?"', line) != []:
            src = re.findall('".*?"', line)[-1]
            tgt = src.replace(',', '').replace('"','')
            rep = line.replace(src, tgt)
            line = rep
        tp = line.split(',')
        line = line.strip()
        imps = float(tp.pop()) # 1 impresson
        clks = float(tp.pop()) # 2 click
        cnvs = float(tp.pop()) # 3 convs
        acpc = float(tp.pop()) # 4 ave_cpc
        week = '___WEEK___' + tp.pop()        # 5 week
        nw2  = tp.pop()        # 6
        nw1  = tp.pop()
        network = '___NETWORK___' + nw1.replace(' ','') + nw2.replace(' ', '')
        adgroup_name = '___ADGROUP_NAME___' + tp.pop().replace(' ', '')
        adgroup = '___ADGROUP___' + str(int(tp.pop()))
        age_range = '___AGE_RANGE___'+tp.pop().replace(' ', '') 
        if imps <= 5. or clks <= 3 or clks/imps >= 1.0 or clks/imps == 0.: continue
        """
        DISP-URLを文字として認識させる
        """
        ts = []
        ts.append(week)
        ts.append(network)
        ts.append(adgroup)
        ts.append(adgroup_name)
        ts.append(age_range)
        print( clks/imps, ','.join(ts))

# 原初の五
# affinity:  affinityフォーマットを処理
# Audience,Ad group ID,Ad group,Network,Network (with search partners),Day of week,Avg. CPC,Conversions,Clicks,Impressions
if '--murakumo' in sys.argv:
    for line in sys.stdin:
        line = line.strip()
        if line == '':continue
        if 'AUDIENCE_PERFORMANCE_REPORT' in line or \
                'Audience,Ad' in line or \
                'Total, --, --, --, --, --,' in line:
                    continue
        import re
        if re.findall('".*?"', line) != []:
            src = re.findall('".*?"', line)[-1]
            tgt = src.replace(',', '').replace('"','')
            rep = line.replace(src, tgt)
            line = rep
        tp = line.split(',')
        line = line.strip()
        imps = float(tp.pop()) # 1 impresson
        clks = float(tp.pop()) # 2 click
        cnvs = float(tp.pop()) # 3 convs
        acpc = float(tp.pop()) # 4 ave_cpc
        week = '___WEEK___' + tp.pop()        # 5 week
        nw2  = tp.pop()        # 6
        nw1  = tp.pop()
        network = '___NETWORK___' + nw1.replace(' ','') + nw2.replace(' ', '')
        adgroup_name = '___ADGROUP_NAME___' + tp.pop().replace(' ', '')
        adgroup = '___ADGROUP___' + str(int(tp.pop()))
        age_range = '___AFFINITY_RANGE___'+tp.pop().replace(' ', '') 
        if imps <= 5. or clks <= 3 or clks/imps >= 1.0 or clks/imps == 0.: continue
        ts = []
        ts.append(week)
        ts.append(network)
        ts.append(adgroup)
        ts.append(adgroup_name)
        ts.append(age_range)
        print( clks/imps, ','.join(ts))

# 原初の五
# gender:  genderフォーマットを処理
# Gender,Ad group ID,Ad group,Network,Network (with search partners),Day of week,Avg. CPC,Conversions,Clicks,Impressions
if '--samidare' in sys.argv:
    for line in sys.stdin:
        line = line.strip()
        if line == '':continue
        if 'Gender,Ad' in line or \
                'GENDER_PERFORMANCE_REPORT' in line or \
                'Total, --, --, --, --, --,' in line:
                    continue
        import re
        if re.findall('".*?"', line) != []:
            src = re.findall('".*?"', line)[-1]
            tgt = src.replace(',', '').replace('"','')
            rep = line.replace(src, tgt)
            line = rep
        tp = line.split(',')
        line = line.strip()
        imps = float(tp.pop()) # 1 impresson
        clks = float(tp.pop()) # 2 click
        cnvs = float(tp.pop()) # 3 convs
        acpc = float(tp.pop()) # 4 ave_cpc
        week = '___WEEK___' + tp.pop()        # 5 week
        nw2  = tp.pop()        # 6
        nw1  = tp.pop()
        network = '___NETWORK___' + nw1.replace(' ','') + nw2.replace(' ', '')
        adgroup_name = '___ADGROUP_NAME___' + tp.pop()
        adgroup = '___ADGROUP___' + str(int(tp.pop()))
        gender = '___GENDER___'+tp.pop().replace(' ', '') 
        if imps <= 5. or clks <= 3 or clks/imps >= 1.0 or clks/imps == 0.: continue
        ts = []
        ts.append(week)
        ts.append(network)
        ts.append(adgroup)
        ts.append(adgroup_name)
        ts.append(gender)
        print( clks/imps, ','.join(ts))

# 原初の五
# text:  textフォーマットを処理
# 
if '--inazuma' in sys.argv:
    m = MeCab.Tagger ("-Owakati")
    for line in sys.stdin:
        line = line.strip()
        if line == '':continue
        if 'AD_PERFORMANCE_REPORT' in line or \
                'Ad,Headline' in line or \
                'Total, --, --, --, --, --,' in line or \
                '.jpg' in line or '.gif' in line:
                    continue
        import re
        if re.findall('".*?"', line) != []:
            src = re.findall('".*?"', line)[-1]
            tgt = src.replace(',', '').replace('"','')
            rep = line.replace(src, tgt)
            line = rep
        tp = line.split(',')
        imps = float(tp.pop()) # 1 impresson
        clks = float(tp.pop()) # 2
        cnvs = float(tp.pop()) # 3
        acpc = '___AVE_COST___' + str(int(float(tp.pop()))) # 4 average cost
        _    = float(tp.pop()) # 5 average cost
        cpcv = '___COST_PER_CONV___' + str(int(float(tp.pop()))) # 6 const per conversion
        apsn = '___AVE_POS___' + str(int(float(tp.pop()))) # average position
        excs = '___EX_CUST_ID___' + str(int(tp.pop())) # Customer ID
        disp = '___URL___' + tp.pop() 
        if imps <= 5. or clks <= 3 or clks/imps >= 1.0 or clks/imps == 0.: continue

        sentence = ' '.join(tp).replace(',', '')
        ts = list(set(m.parse(sentence).strip().split(' ')))
        """
        DISP-URLを文字として認識させる
        """
        ts.append(disp)
        ts.append(excs)
        ts.append(apsn)
        ts.append(cpcv)
        ts.append(acpc)

        print( clks/imps, ','.join(ts))

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
                '.jpg' in line:
                    continue
        import re
        if re.findall('".*?"', line) != []:
            src = re.findall('".*?"', line)[-1]
            tgt = src.replace(',', '').replace('"','')
            rep = line.replace(src, tgt)
            line = rep
        tp = line.split(',')
        try:
          imps = float(tp.pop()) # 1 impresson
          clks = float(tp.pop()) # 2
          cnvs = float(tp.pop()) # 3
          acpc = float(tp.pop()) # 4
          _    = float(tp.pop()) # 5
          cpcv = float(tp.pop()) # 6
          apsn = '___APOS___' + str(float(tp.pop())) 
          excs = '___EXCUST___' + str(int(tp.pop()))
          disp = '___URL___' + tp.pop() 
        except:
          #print( line )
          continue

        if imps <= 5. or clks <= 5 or clks/imps >= 1.0 or clks/imps == 0.: continue

        sentence = ' '.join(tp).replace(',', '')
        ts = m.parse(sentence).strip().split(' ')
        """
        DISP-URLを文字として認識させる
        """
        ts.append(disp)
        ts.append(excs)
        ts.append(apsn)
        tf = C(ts)
        output = []
        for t,f in tf.items():
          """
          1に正則化かしないか、決める
          """
          #output.append( ':'.join(map(str, [ti[t], idf[t]*f])) )
          output.append( ':'.join(map(str, [ti[t], 1.])) )
        output_txt = " ".join(sorted(output, key=lambda x:int(x.split(':')[0])))
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

if '--kagerou' in sys.argv:
    import cPickle as P
    it = P.loads(open('it.p').read())
    tw = {}
    lines = open('result.txt').read().split('\n')
    weights = map(float, lines[1].split(','))
    for i, w in enumerate(weights):
        tw[it[i]] = w
    for t, w in sorted(tw.items(), key=lambda x:x[1]*-1):
        print(t,w)
    print(len(weights))
    print(len(it.keys()))
    #print((set(it.values()) - set(tw.keys())).pop())
        
