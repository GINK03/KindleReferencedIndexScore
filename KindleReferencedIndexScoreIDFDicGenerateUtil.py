# coding: utf-8
from __future__ import print_function
import sys
"""
形態そ解析された標準入力に対して、一行一コンテンツとして仮定して、IDF辞書を作成する
"""
if __name__ == '__main__':
    all_words = set()
    dics      = []
    for i, line in enumerate(sys.stdin):
        line = line[:-1].split(',').pop().strip()
        dic = set(line.split(' ') )
        if len(dic) == 1:
            continue
        [all_words.add(e) for e in dic]
        #print( i, len(all_words), len(dics) )
        dics.append(dic)


    # 転置させてidfがどのようになっているか確認する
    D = len(dics)
    results = []
    for i, w in enumerate(all_words):
        c = 0
        for dic in dics:
            if w in dic:
                c += 1
        if D < c:
            print(w, D, c, i, len(all_words) )
