# coding: utf-8

import os
import sys
import gensim
import gensim.models.doc2vec as doc2vec
LS = doc2vec.LabeledSentence
D2V = doc2vec.Doc2Vec
import math
import itertools

docs = [
    ['human', 'interface', 'computer'],
    ['survey', 'user', 'computer', 'system', 'response', 'time'],
    ['eps', 'user', 'interface', 'system'],
    ['system', 'human', 'system', 'eps'],
    ['user', 'response', 'time'],
    ['trees'],
    ['graph', 'trees'],
    ['graph', 'minors', 'trees'],
    ['graph', 'minors', 'survey'] 
]


def main():
  doc = list(map(lambda x:LS(words=docs[x[0]], tags=[x[0]]), enumerate(docs)))
  model = D2V(doc, size=100, window=300, workers=4, min_count=0)
  pass

if __name__ == '__main__':
  main()
