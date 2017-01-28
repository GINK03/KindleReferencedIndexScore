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
if args.gpu >= 0:
    for key, value in list(state.items()):
        value.data = cuda.to_gpu(value.data)
if args.gpu >= 0:
    prev_char = cuda.to_gpu(prev_char)
# print('\n dumping...', i, end= " ")
from copy import deepcopy as DC
""" stateを初期化 """
i = vocab["iPhone"]
prev_char = np.array([i], dtype=np.int32)
prev_char_stack  = []
prev_ichar_stack = [ivocab[i]]
state = make_initial_state(n_units, batchsize=1, train=False)
state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)
beam = {ivocab[i]: [DC(state), DC(prob), 1.]}
for i in range(30):
    probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
    probability /= np.sum(probability)
    prob_with_index = []
    for e, p in enumerate(probability):
        prob_with_index.append( [e, p, ivocab[e] ] )
    prob_with_index.sort(key=lambda x:-1 * x[1] )
    
    index1     = prob_with_index[0][0]
    chosen_p1  = probability[index1]
    prev_char1 = np.array([index1], dtype=np.int32)

    prev_char = prev_char1
    state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)
    
    prev_ichar_stack.append(ivocab[index1])
    prev_char_stack.append(prev_char1)

    key=':'.join(prev_ichar_stack)
    val=[DC(state), prob, chosen_p1] 
    beam[key] = val

    if '<EOS>' == ivocab[index1]:
        #print(ivocab[index1], end="\n")
        break
    else:
        #print(ivocab[index1], end="")
        pass
#print('\n'.join(beam.keys()))
#print(beam)
for k in range(1, 14):
    beam_buff = DC(beam)
    for key, val in beam.items():
        if '<EOS>' in key:
            #print(key)
            continue
        prev_ichar_stack = key.split(':')
        state, prob, chosen_p = val 
        probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
        probability /= np.sum(probability)
        prob_with_index = []
        for e, p in enumerate(probability):
            prob_with_index.append( [e, p, ivocab[e] ] )
        prob_with_index.sort(key=lambda x:-1 * x[1] )
       
        improval = False
        for l in range(3):
            """ icharをキャッシュ """
            ichar_cache = DC(prev_ichar_stack)

            """ ここをインクリメントする """
            index     = prob_with_index[l][0]
            chosen_p  = probability[index]
            prev_char = np.array([index], dtype=np.int32)
        
            """ stateをアップデート """
            ichar_cache.append(ivocab[index])

            check_key = ':'.join(ichar_cache)
            if beam_buff.get(check_key) == None: 
                #print('input', key, 'GEN', check_key)
                if '<EOS>' in check_key:
                    #print('GENERATED', check_key)
                    pass
                prev_ichar_stack = ichar_cache
                improval = True
                break

        if improval == True:
            state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)

            key=':'.join(prev_ichar_stack)
            val=[DC(state), DC(prob), DC(chosen_p)] 
            beam_buff[key] = val
    beam = beam_buff
#print(beam)

for key, val in sorted(beam.items(), key=lambda x:len(x[0])):
    print(key, '%5.9f'%math.log(val[2] + 0.00000000001))

max_depth = max(map(lambda x:len(x.split(':')), beam.keys()))
print('max_depth', max_depth)

head = list(beam.keys()).pop().split(':').pop(0)
print(head)
start =  { 'name': head , 'children': [] }
for node in range(1, max_depth):
    for txt in sorted(beam.keys(), key=lambda x:len(x)):
        print("txt", txt)
        try:
            head = txt.split(':')[node]
        except :
            continue
        search = start
        for inner in range(1, node):
            inner_key = txt.split(':')[inner]
            inner_children = search['children']
            inner_names = map(lambda x:x.get('name'), inner_children)
            if inner_key not in inner_names:
                search['children'].append( { 'name': inner_key , 'children': [] } )
                search = list(filter(lambda x:x['name'] == inner_key,search['children']))[0]
            else:
                search = list(filter(lambda x:x.get('name') == inner_key, inner_children))[0]
        if list(filter(lambda x:x.get('name') == head, search['children'])) == []:
            search['children'].append(  { 'name': head , 'children': [] } )

import json
import re
"""
Adhoc regex
"""
fixed = re.sub('"children": \[\]', '"size": 100', json.dumps(start))
print(fixed)

