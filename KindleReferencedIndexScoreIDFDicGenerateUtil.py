# coding: utf-8
from __future__ import print_function
import sys
import re
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
        fdic = set()
        for d in dic:
          """
          [で始まって否く、\sを持っていたら、その単語は多分問題あり
          """
          if ' ' in d and '[info]' in d:
            d = re.sub('\[info\]\sall_tf,\s.{1,}\s', '', d) 
            fdic.add(d)
          else:
            fdic.add(d)
        [all_words.add(e) for e in fdic]
        dics  += 1
        for t in fdic:
          if 'info' in t:
            #print(t)
            #sys.exit(0)
            pass
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
        print('___'.join( map(lambda x:str(x), [w, D, c, i, len(all_words), ','.join(map(lambda x:x, asin_freq))] )  ) )
