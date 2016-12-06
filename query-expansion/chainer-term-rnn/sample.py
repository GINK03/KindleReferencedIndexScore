# coding: utf-8
import time
import math
import sys
import argparse
import pickle as pickle
import codecs

import numpy as np
from chainer import cuda, Variable, FunctionSet
import chainer.functions as F
from CharRNN import CharRNN, make_initial_state

#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

#%% arguments
parser = argparse.ArgumentParser()

parser.add_argument('--model',      type=str,   required=True)
parser.add_argument('--vocabulary', type=str,   required=True)

parser.add_argument('--seed',       type=int,   default=123)
parser.add_argument('--sample',     type=int,   default=1)
parser.add_argument('--primetext',  type=str,   default='')
parser.add_argument('--length',     type=int,   default=2000)
parser.add_argument('--gpu',        type=int,   default=-1)

args = parser.parse_args()

np.random.seed(args.seed)

# load vocabulary
vocab = pickle.load(open(args.vocabulary, 'rb'))
#print(vocab)
#print(' '.join(vocab.keys()))
ivocab = {}
for e, (c, i) in enumerate(vocab.items()):
    #print e, c.decode('utf-8')
    ivocab[i] = c
## sys.exit(0)
# load model
model = pickle.load(open(args.model, 'rb'))
n_units = model.embed.W.data.shape[1]

if args.gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()

# initialize generator
state = make_initial_state(n_units, batchsize=1, train=False)
if args.gpu >= 0:
    for key, value in list(state.items()):
        value.data = cuda.to_gpu(value.data)

prev_char = np.array([0], dtype=np.int32)
if args.gpu >= 0:
    prev_char = cuda.to_gpu(prev_char)

if len(args.primetext) > 0:
    #for i in unicode(args.primetext, 'utf-8'):
    for i in ['2']:
        #sys.stdout.write(i)
        print(i.decode('utf-8'))
        #prev_char = np.ones((1,), dtype=np.int32) * vocab[i.encode('utf-8')]
        prev_char = np.ones((1,), dtype=np.int32) * vocab[i]
        print('prev char ', prev_char)
        if args.gpu >= 0:
            prev_char = cuda.to_gpu(prev_char)

        state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)

#for i in range(args.length):
prev_char_stack = []
result = []
for j in range(10):
  state = make_initial_state(n_units, batchsize=1, train=False)
  #print('\niter ', j) 
  print('\n dumping...', i, end= " ")
  for i in range(300):
    if i == 0 and j != 0:
      import random
      for _pc in prev_char_stack[-int(50*random.random()):]:
        state, prob = model.forward_one_step(_pc, _pc, state, train=False)
    else:
      state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)


    #if args.sample > 0:
    probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
    probability /= np.sum(probability)
    prob_with_index = []
    for e, p in enumerate(probability):
        prob_with_index.append( [e, p, ivocab[e] ] )
    prob_with_index.sort(key=lambda x:-1 * x[1] )
    """
    ランダムチョイス
    """
    index = np.random.choice(list(range(len(probability))), p=probability)
    """
    最大値チョイス(結構うまくいく)
    """
    index = prob_with_index[0][0]
    chosen_p = probability[index]
    """
    TOP N random select
    """
    probs = [prob_with_index[0][1], prob_with_index[1][1]]
    probs = [probs[0]/sum(probs), probs[1]/sum(probs)]
    import random
    saikoro = 0
    """
    任意のワードが支配的になってしまうことを防ぐ
    """
    index = prob_with_index[saikoro][0]
    if ivocab[index] in ['そ', '俺']:
        if random.random() < 0.5:
            saikoro = 1
    if random.random() < 0.05:
        saikoro = 1
    index = prob_with_index[saikoro][0]
        
    #print("try", i, "vocindex", index, "probability", chosen_p, "voc", ivocab[index])
    print(ivocab[index], end="")
    result.append(ivocab[index])
    top_n_p_sum = 0.
    n_p_var = np.var(probability)
    for e, p, t in prob_with_index[0:10]:
        #print("candidate", e, p, t)
        top_n_p_sum += p
    top_n_p_sum /= 10.
    #print("  average of top 10's prob sum", top_n_p_sum)
    #print("  probability's variance ", n_p_var)
    prev_char = np.array([index], dtype=np.int32)
    if args.gpu >= 0:
        prev_char = cuda.to_gpu(prev_char)
    
    prev_char_stack.append(prev_char)

print()
import regex
print( regex.sub('\s','\n ', ''.join(result)) )
print( ''.join(result) )
