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
import glob
if "deep" == "deep":
    from DeepRNN import DeepRNN as CharRNN
    #from DeepRNN import make_initial_state
    make_initial_state = CharRNN.make_initial_state
else:
    from CharRNN import CharRNN, make_initial_state

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, default='data/bad_apple')  
args = parser.parse_args()

INPUTS = """
./data/liarufanclub/*.chainermodel,./data/liarufanclub/vocab.bin
./data/bad_apple/*.chainermodel,./data/bad_apple/vocab.bin
./data/lostone/*.chainermodel,./data/lostone/vocab.bin
./data/senbonzakura/*.chainermodel,./data/senbonzakura/vocab.bin
"""
vocabs = []
for vocab_filename in map(lambda x:x.split(',')[1], filter(lambda x:x!='', INPUTS.split('\n'))):
    vocabs.append( \
                pickle.load(open(vocab_filename, 'rb')) \
            )

models = []
for model_filename in map(lambda x:x.split(',')[0], filter(lambda x:x!='', INPUTS.split('\n'))):
    models.append( \
                pickle.load(open(glob.glob(model_filename).pop(), 'rb')) \
            )


class TextList:
    def __init__(self, data):
        self.data = data
        self.before_rank = None
        self.before_prob = None
        self.state = None
        self.model = None 
        self.ivocab = {}
    def update_data(self, vocab=None, model=None, inputs=None):
        if inputs is not None:
            data = [term if vocab.get(term) != None else "___UNK___" for term in self.data]
            self.data = data
        else:
            self.data = self.data
    
    def init_state(self, model=None, vocab=None):
        self.model = model
        self.vocab = vocab 
        n_units = self.model.embed.W.data.shape[1]
        self.state =  make_initial_state(n_units, batchsize=1, train=False)
        for e, (c, i) in enumerate(self.vocab.items()):
            self.ivocab[i] = c
    def process_state(self):
        # stateの状態を作成する
        for index, term in [(self.vocab.get(term),term) for term in self.data]:
            #print(term, end="")
            char = np.array([index], dtype=np.int32)
            self.state, prob = self.model.forward_one_step(char, char, self.state, train=False)
            probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
            probability /= np.sum(probability)
            prob_with_term = []
            for e, p in enumerate(probability):
                prob_with_term.append( [p, self.ivocab[e] ] )
            prob_with_term = sorted(prob_with_term, key=lambda x:-1 * x[0] )[:10]
            
            prob_term = {}
            for e, p in enumerate(probability):
                prob_term[self.ivocab[e]] = p
        return prob_term
        # stateから予想を行う
    def predict(self, term=None):
        index = self.vocab[term]
        char = np.array([index], dtype=np.int32)
        self.state, prob = self.model.forward_one_step(char, char, self.state, train=False)
        probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
        probability /= np.sum(probability)
        prob_term = {}
        for e, p in enumerate(probability):
            prob_term[self.ivocab[e]] = p
        return prob_term

def model_initializer(data=None, model=None, vocab=None):
    tl = TextList(data)
    tl.init_state(vocab=vocab, model=model)
    tl.update_data(vocab=vocab, model=model, inputs=None)
    return tl

def predicter(tl=None):
    prob_term = tl.process_state()
    yield prob_term
    maxprob_term  = sorted(prob_term.items(), key=lambda x:x[1]*-1)[0][0]

if __name__ == '__main__':
    data = ['v100', 'q100']
    print(''.join(data), end="")
    instances = [model_initializer(data=data, model=model, vocab=vocab) for model, vocab in zip(models, vocabs)]
    t_ps = [t_p for t_p in map(lambda x:x.process_state(), instances)]
    t_ps = list(zip(t_ps, [1, 0.1, 0.1, 0.1]))
    t_p_sum = {}
    for t_p, w in t_ps:
        for t in t_p.keys(): t_p_sum[t] = 0.
    for t_p, w in t_ps:
        for t,p in t_p.items():
            t_p_sum[t] += p
    chosen = sorted( t_p_sum.items(), key=lambda x:x[1]*-1)[0][0]
    #print(t_p_sum)
    for _ in range(100):
        print(chosen, end="")
        t_ps = [ tl.predict(term=chosen) for tl in instances ]        
        t_ps = list(zip(t_ps, [1, 0.1, 0.1, 0.1]))
        t_p_sum = {}
        for t_p, w in t_ps:
            for t in t_p.keys(): t_p_sum[t] = 0.
        for t_p, w in t_ps:
            for t,p in t_p.items():
                t_p_sum[t] += p
        chosen = sorted( t_p_sum.items(), key=lambda x:x[1]*-1)[0][0]
    print()
    print("end")


if __name__ == '__test__':
    TextList.init_state()
    TextList.update_data("この情報は初期値なので任意の文字列に入れ替えてください。fuckin hot")
    state = TextList.process_state()
