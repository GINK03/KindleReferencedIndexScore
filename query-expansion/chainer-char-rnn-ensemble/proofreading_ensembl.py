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
#parser.add_argument('--model',      type=str,   required=True)
parser.add_argument('--seed',       type=int,   default=123)
parser.add_argument('--sample',     type=int,   default=1)
parser.add_argument('--primetext',  type=str,   default='')
parser.add_argument('--length',     type=int,   default=2000)
parser.add_argument('--gpu',        type=int,   default=-1)
parser.add_argument('--text',       type=str,   default='')
parser.add_argument('--vocabulary',       type=str,   default='')
args = parser.parse_args()
mt = MeCab.Tagger('-Owakati')
text = args.text
res = mt.parse(text).strip()
print 'input', res
inputs = res.split(' ')

np.random.seed(args.seed)

vocab1 = pickle.load(open('./data/ensembl1/vocab.bin', 'rb'))
vocab2 = pickle.load(open('./data/ensembl2/vocab.bin', 'rb'))
vocab3 = pickle.load(open('./data/ensembl3/vocab.bin', 'rb'))
vocab4 = pickle.load(open('./data/ensembl4/vocab.bin', 'rb'))
inputs_index1 = []
inputs_index2 = []
inputs_index3 = []
inputs_index4 = []
ivocab1 = {}
ivocab2 = {}
ivocab3 = {}
ivocab4 = {}
model1 = pickle.load(open('./cv/latest_ensembl1_128.chainermodel', 'rb'))
model2 = pickle.load(open('./cv/latest_ensembl2_128.chainermodel', 'rb'))
model3 = pickle.load(open('./cv/latest_ensembl3_128.chainermodel', 'rb'))
model4 = pickle.load(open('./cv/latest_ensembl4_128.chainermodel', 'rb'))
n_units1 = model1.embed.W.data.shape[1]
n_units2 = model2.embed.W.data.shape[1]
n_units3 = model3.embed.W.data.shape[1]
n_units4 = model4.embed.W.data.shape[1]

# initialize generator
state1 = make_initial_state(n_units1, batchsize=1, train=False)
state2 = make_initial_state(n_units2, batchsize=1, train=False)
state3 = make_initial_state(n_units3, batchsize=1, train=False)
state4 = make_initial_state(n_units4, batchsize=1, train=False)

for vocab, inputs_index in [ (vocab1, inputs_index1), (vocab2, inputs_index2), (vocab3, inputs_index3), (vocab4, inputs_index4) ]:
  for word in inputs:
    if vocab.get(word) != None:
      inputs_index.append( vocab.get(word) ) 
    else:
      print word,  "is not found."
      inputs_index.append( 'UNK' )
for vocab, ivocab in [ (vocab1, ivocab1), (vocab2, ivocab2), (vocab3, ivocab3), (vocab4, ivocab4)]:
  for e, (c, i) in enumerate(vocab.items()):
    ivocab[i] = c

probability_ensembl = []

for _ in range(len(inputs)):
    probability_ensembl.append( list() )

for (model, state, ivocab, inputs_index) in [(model1, state1, ivocab1, inputs_index1), (model2, state2, ivocab2, inputs_index2), (model3, state3, ivocab3, inputs_index3), (model4, state4, ivocab4, inputs_index4)] :
    if args.gpu >= 0:
        cuda.get_device(args.gpu).use()
        model.to_gpu()
    if args.gpu >= 0:
        for key, value in state.items():
            value.data = cuda.to_gpu(value.data)
    prev_char = np.array([0], dtype=np.int32)
    if args.gpu >= 0:
        prev_char = cuda.to_gpu(prev_char)
    chosen_ps = []
    for i in range(len(inputs_index)):
        state, prob = model.forward_one_step(prev_char, prev_char, state, train=False)
        probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
        probability /= np.sum(probability)
        prob_with_index = []
        for e, p in enumerate(probability):
            try:
                prob_with_index.append( [e, p, ivocab[e].decode('utf-8') ] )
            except:
                pass
        prob_with_index.sort(key=lambda x:-1 * x[1] )
        index = inputs_index[i]
        #print "index", index
        #print inputs_index
        #sys.exit(0)
        if 'UNK' != index:
          chosen_p = probability[index]
          chosen_ps.append(chosen_p)
        else:
          chosen_p = 0.
          chosen_ps.append(0.)
        #print "try", i, "vocindex", index, "probability", chosen_p, "voc", (lambda x: ivocab[index].decode('utf-8') if index != 'UNK' else 'UNK')(None)

        # 確率値を保存
        probability_ensembl[i].append(chosen_p)
        """ 
        top_n_p_sum = 0.
        n_p_var = np.var(probability)
        for e, p, t in prob_with_index[0:10]:
            print "candidate", e, p, t
            top_n_p_sum += p
        top_n_p_sum /= 10.
        print "  average of top 10's prob sum", top_n_p_sum
        print "  probability's variance ", n_p_var
        """
        if index != 'UNK':
          prev_char = np.array([index], dtype=np.int32)
          if args.gpu >= 0:
            prev_char = cuda.to_gpu(prev_char)

#print 'chosen_ps =', ' '.join(map(str, chosen_ps))
import json
print 'ensembl_ps = ', str(json.dumps(probability_ensembl) )
print
