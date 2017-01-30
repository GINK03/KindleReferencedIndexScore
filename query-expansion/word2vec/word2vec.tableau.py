# coding: utf-8
from __future__ import print_function
import os
import math
import gensim
from gensim.models import word2vec
import sys
from itertools import permutations as P
from itertools import combinations_with_replacement as CR

def main():
  if '--train' in sys.argv:
    fname = list(filter(lambda x:'--input=' in x, sys.argv))[0].split('=').pop()
    txts = []
    for txt in filter(lambda x:'' != x, open(fname).read().split('\n')):
        term, num = txt.split(',')
        term, num = term, int(num)
        txts.append( (("%s "%term)*num) ) 

    source = [ ' '.join(txts).split() ]
    model = word2vec.Word2Vec(source, size=100, window=5, min_count=5, workers=4)
    model.save(fname + '.w2v')

    out=model.most_similar(positive=['ア'])
    for x in out:
      #print(x[0],x[1])
      pass
   

    unique = set( source.pop() )
    for head, tail in CR(unique, 2):
        print(head, tail, model.similarity(head, tail) )
    
if __name__ == '__main__':
    main()
