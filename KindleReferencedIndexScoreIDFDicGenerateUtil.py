# coding: utf-8
from __future__ import print_function
import sys
"""
形態そ解析された標準入力に対して、一行一コンテンツとして仮定して、IDF辞書を作成する
"""
if __name__ == '__main__':
    all_words = set()
    dics      = 0
    #asin_term_freq = {}
    term_asin      = {}
    for i, line in enumerate(sys.stdin):
        line = line.strip()
        if not '[info] all_tf' in line:
          continue
        """
        use triple spaces to deliminate
        """

        ents = line.split('   ')
        asin = line.split(' ')[2]
        tf_raw = filter(lambda x: '///' in x, ents)
        if len(asin ) != 10 :
          continue
        dic   = set(map(lambda x:x.split('///').pop(0), tf_raw ) )
        [all_words.add(e) for e in dic]
        dics  += 1
        #tfdic = dict( [ (x.split('///')[0], x.split('///')[1] ) for x in tf_raw ] )
        #asin_term_freq.update( {asin: tfdic} )
        for t in dic:
          if term_asin.get(t) == None:
           term_asin.update({t: asin })
          else:
           term_asin[t] += ',' + asin

    # 転置させてidfがどのようになっているか確認する
    D = dics
    results = []
    for i, w in enumerate(all_words):
        c = 0
        asin_freq = []
        c = len( term_asin[w].split(',') )
        asins = term_asin[w].split(',')
        for asin in asins:
          asin_freq.append( asin )
        print(w, D, c, i, len(all_words), ','.join(map(lambda x:x, asin_freq)) )
