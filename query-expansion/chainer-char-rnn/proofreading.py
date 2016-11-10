#coding:utf-8
import time
import math
import sys
import argparse
import cPickle as pickle
import codecs

import numpy as np
from chainer import cuda, Variable, FunctionSet
import chainer.functions as F
from CharRNN import CharRNN, make_initial_state

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
reload(sys)
sys.setdefaultencoding('utf-8')

import MeCab

parser = argparse.ArgumentParser()
parser.add_argument('--model',      type=str,   required=True)
parser.add_argument('--vocabulary', type=str,   required=True)
parser.add_argument('--seed',       type=int,   default=123)
parser.add_argument('--sample',     type=int,   default=1)
parser.add_argument('--primetext',  type=str,   default='')
parser.add_argument('--length',     type=int,   default=2000)
parser.add_argument('--gpu',        type=int,   default=-1)

args = parser.parse_args()

# 形態素解析して、日本語を分解する
mt = MeCab.Tagger('-Owakati')
text = "話し言葉や書き言葉と同一の言語である"
res = mt.parse(text).strip()
print 'input', res
inputs = res.split(' ')

np.random.seed(args.seed)

# load vocabulary
vocab = pickle.load(open(args.vocabulary, 'rb'))
# 日本語をvocab indexに変換

inputs_index = []
for word in inputs:
  if vocab.get(word):
    inputs_index.append( vocab.get(word) ) 
  else:
    inputs_index.append( 'UNK' )
print inputs
print inputs_index
#print(vocab)
ivocab = {}
for e, (c, i) in enumerate(vocab.items()):
    #print e, c.decode('utf-8')
    ivocab[i] = c
# load model
model = pickle.load(open(args.model, 'rb'))
n_units = model.embed.W.data.shape[1]

if args.gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()

# initialize generator
state = make_initial_state(n_units, batchsize=1, train=False)
if args.gpu >= 0:
    for key, value in state.items():
        value.data = cuda.to_gpu(value.data)

prev_char = np.array([0], dtype=np.int32)
if args.gpu >= 0:
    prev_char = cuda.to_gpu(prev_char)


for i in xrange(len(inputs_index)):
    state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)

    #if args.sample > 0:
    probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
    probability /= np.sum(probability)
    prob_with_index = []
    for e, p in enumerate(probability):
        prob_with_index.append( [e, p, ivocab[e].decode('utf-8') ] )
    prob_with_index.sort(key=lambda x:-1 * x[1] )
    #index = np.random.choice(range(len(probability)), p=probability)
    index = inputs_index[i]
    chosen_p = probability[index]
    #else:
    #    index = np.argmax(cuda.to_cpu(prob.data))
    
    #sys.stdout.write(ivocab[index].decode('utf-8'))
    print "try", i, "vocindex", index, "probability", chosen_p, "voc", ivocab[index].decode('utf-8')
    top_n_p_sum = 0.
    n_p_var = np.var(probability)
    for e, p, t in prob_with_index[0:10]:
        print "candidate", e, p, t
        top_n_p_sum += p
    top_n_p_sum /= 10.
    print "  average of top 10's prob sum", top_n_p_sum
    print "  probability's variance ", n_p_var
    prev_char = np.array([index], dtype=np.int32)
    if args.gpu >= 0:
        prev_char = cuda.to_gpu(prev_char)

print
