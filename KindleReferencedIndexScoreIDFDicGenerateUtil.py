# coding: utf-8
from __future__ import print_function
import sys
"""
形態そ解析された標準入力に対して、一行一コンテンツとして仮定して、IDF辞書を作成する
"""
if __name__ == '__main__':
    all_words = set()
    dics      = []
    asin_term_freq = {}
    for i, line in enumerate(sys.stdin):
        line = line[:-1].split(',').pop().strip()
        if not '|' in line:
          continue
        ents = line.split(' ')
        asin = ents.pop(0)
        if len(asin ) != 10 :
          continue
        wf    = filter(lambda x:'|' in x, ents)
        dic   = set(map(lambda x:x.split('|').pop(0), wf ) )
        [all_words.add(e) for e in dic]
        #print( i, len(all_words), len(dics) )
        dics.append({'dic':dic, 'asin':asin} )
        tfdic = dict( [ (x.split('|')[0], x.split('|')[1] ) for x in wf ] )
        asin_term_freq.update( {asin: tfdic} )
        #print(asin_term_freq[asin])

    # 転置させてidfがどのようになっているか確認する
    D = len(dics)
    results = []
    for i, w in enumerate(all_words):
        c = 0
        asins = []
        for dic in dics:
            if w in dic['dic']:
                if asin_term_freq.get(dic['asin']) and asin_term_freq.get(dic['asin']).get(w):
                  c += 1
                  asins.append( (dic['asin'], asin_term_freq[dic['asin']][w] ) )
        print(w, D, c, i, len(all_words), ','.join(map(lambda x:x[0] + '/' + x[1], asins)) )
