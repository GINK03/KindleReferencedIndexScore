# coding: utf-8
from __future__ import print_function
import sys
import os
import regex
import bs4
import urllib2
import urllib 
import httplib
import ssl 
import multiprocessing as mp
from socket import error as SocketError
import plyvel
import cPickle as pickle
import copy
import gensim
from gensim.models import *

if __name__ == '__main__':
  sentences = list()
  tag_sentence = {}
  count = 0
  buff = ''
  for i,line in enumerate(open('./narou.src.txt').read().split('\n')):
    buff += line
    if i%10 == 0:
      sentences.append(doc2vec.LabeledSentence(words=[e for e in buff.split(' ')], tags=[u'SENT_' + str(count)]) )
      tag_sentence.update({u'SENT_' + str(count): [e for e in buff.split(' ')]}) 
      count+=1
      buff = ''
  if '--learn' in sys.argv:
    print(sentences)
    model = Doc2Vec(alpha=0.025, min_alpha=0.025, min_count=1) 
    model.build_vocab(sentences)
    for epoch in range(10):
      model.train(sentences)
      model.alpha -= 0.002  # decrease the learning rate
      model.min_alpha = model.alpha  # fix the learning rate, no decay
    model.save("model.doc2vec")
  if '-e' in sys.argv:
    num = filter(lambda x:x.isdigit(), sys.argv).pop()
    model = Doc2Vec.load('model.doc2vec')
    tag = u'SENT_' + num
    res = model.docvecs.most_similar([tag])
    print(tag, ''.join(tag_sentence[tag]) )
    for tag, cosine in res:
      print(tag, cosine, ''.join(tag_sentence[tag]))
