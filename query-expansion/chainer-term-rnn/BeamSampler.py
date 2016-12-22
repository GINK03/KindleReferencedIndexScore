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
vocab = pickle.load(open(args.vocabulary, 'rb'))
ivocab = {}
for e, (c, i) in enumerate(vocab.items()):
    ivocab[i] = c
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
prev_char_stack = []
prev_ichar_stack = []
state = make_initial_state(n_units, batchsize=1, train=False)
print('\n dumping...', i, end= " ")
for i in range(300):
    state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)
    probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
    probability /= np.sum(probability)
    prob_with_index = []
    for e, p in enumerate(probability):
        prob_with_index.append( [e, p, ivocab[e] ] )
    prob_with_index.sort(key=lambda x:-1 * x[1] )
    """
    最大値チョイス(結構うまくいく)
    """
    index = prob_with_index[0][0]
    chosen_p = probability[index]
    print(ivocab[index], end="")
    prev_ichar_stack.append(ivocab[index])
    top_n_p_sum = 0.
    n_p_var = np.var(probability)
    for e, p, t in prob_with_index[0:10]:
        top_n_p_sum += p
    top_n_p_sum /= 10.
    prev_char = np.array([index], dtype=np.int32)
    if args.gpu >= 0:
        prev_char = cuda.to_gpu(prev_char)
    prev_char_stack.append(prev_char)
print()
