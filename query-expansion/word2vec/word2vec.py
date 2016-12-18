# coding: utf-8
import os
import math
import gensim
from gensim.models import word2vec
import sys

if __name__ == '__main__':
    fname = sys.argv[1]
    print fname
    data = word2vec.Text8Corpus(fname) 
    model = word2vec.Word2Vec(data, size=100, window=5, min_count=5, workers=4)
    model.save(fname + '.w2v')

    out=model.most_similar(positive=['艦これ'.decode('utf-8')])
    for x in out:
            print x[0],x[1]
