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

if "deep" == "deep":
    from DeepRNN import DeepRNN as CharRNN
    #from DeepRNN import make_initial_state
    make_initial_state = CharRNN.make_initial_state
else:
    from CharRNN import CharRNN, make_initial_state

vocab = pickle.load(open('./data/tinyshakespeare/vocab.bin', 'rb'))
ivocab = {}
for e, (c, i) in enumerate(vocab.items()):
    ivocab[i] = c
model = pickle.load(open('./data/tinyshakespeare/latest_deeprnn_tinyshakespeare_768.chainermodel', 'rb'))

n_units = model.embed.W.data.shape[1]
prev_char = np.array([0], dtype=np.int32)

class TextList:
    data = ['this', 'is', 'a']
    before_rank = None
    before_prob = None
    state = None
    @staticmethod
    def update_data(inputs=""):
        data = [term if vocab.get(term) != None else "___UNK___" for term in TextList.data]
        TextList.data = data
    @staticmethod
    def init_state():
        TextList.state =  make_initial_state(n_units, batchsize=1, train=False)
    @staticmethod
    def process_state():
        # stateの状態を作成する
        for index, term in [(vocab.get(term),term) for term in TextList.data]:
            print("input", term)
            char = np.array([index], dtype=np.int32)
            TextList.state, prob = model.forward_one_step(char, char, TextList.state, train=False)
            probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
            probability /= np.sum(probability)
            prob_with_term = []
            for e, p in enumerate(probability):
                prob_with_term.append( [p, ivocab[e] ] )
            prob_with_term = sorted(prob_with_term, key=lambda x:-1 * x[0] )[:10]
        prob, term = prob_with_term[0]
        
        # stateから予想を行う
        for _ in range(100):
            index = vocab.get(term)
            char = np.array([index], dtype=np.int32)
            TextList.state, prob = model.forward_one_step(char, char, TextList.state, train=False)
            probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
            probability /= np.sum(probability)
            prob_with_term = []
            for e, p in enumerate(probability):
                prob_with_term.append( [p, ivocab[e] ] )
            prob_with_term = sorted(prob_with_term, key=lambda x:-1 * x[0] )[:10]
            # termのアップデート
            prob, term = prob_with_term[0]
            print(term, end=" ")
            
        return TextList.state

if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if line == '' or 'http' in line: continue
        TextList.init_state()
        line = line.strip()
        TextList.update_data(line)
        state = TextList.process_state()


if __name__ == '__test__':
    TextList.init_state()
    TextList.update_data("この情報は初期値なので任意の文字列に入れ替えてください。fuckin hot")
    state = TextList.process_state()
