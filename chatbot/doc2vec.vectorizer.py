# coding: utf-8

import os
import sys
import gensim
import gensim.models.doc2vec as doc2vec
LS = doc2vec.LabeledSentence
D2V = doc2vec.Doc2Vec
import math
import itertools
import MeCab
import numpy as np
t = MeCab.Tagger('-Owakati')


def main():
  docs = [t.parse(line.strip()).split() for line in open('./sample/input.txt').read().split('\n')]
  doc = map(lambda x:LS(words=docs[x[0]], tags=[x[0]]), enumerate(docs))
  model = D2V(doc, size=100, window=300, workers=4, min_count=0)
  model.save('./sample/sample.model')
  pass

def load():
  model = D2V.load('./sample/sample.model')
  docs = [t.parse(line.strip()).split() for line in open('./sample/input.txt').read().split('\n')]
  target_vec = model.infer_vector(docs[0]) 
  #print("target_vec", target_vec)
  #print("source_vec", source_vec)
  for i, doc in enumerate(docs):
      source_vec = model.infer_vector(doc)
      similarity = np.dot(target_vec, source_vec)/ (np.linalg.norm(target_vec)*np.linalg.norm(source_vec))
      print("i", i, "dot", similarity)
if __name__ == '__main__':
  main()
  load()
