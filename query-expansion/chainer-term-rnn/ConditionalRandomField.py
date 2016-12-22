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

vocab = pickle.load(open('/home/gimpei/KindleReferencedIndexScore/query-expansion/chainer-term-rnn/data/middlesuumo/vocab.bin', 'rb'))
ivocab = {}
for e, (c, i) in enumerate(vocab.items()):
    ivocab[i] = c
model = pickle.load(open('/home/gimpei/KindleReferencedIndexScore/query-expansion/chainer-term-rnn/data/middlesuumo/latest_middlesuumo_768.chainermodel', 'rb'))
n_units = model.embed.W.data.shape[1]
prev_char = np.array([0], dtype=np.int32)
"""
校正対象の文字を読み込み
"""
class TextList:
    data = ['これ', 'は', 'デフォルト', 'の', '情報', 'です']
    before_rank = None
    before_prob = None
    state = None
    @staticmethod
    def update_data(inputs=""):
        from MeCab import Tagger
        t = Tagger('-Owakati')
        data = [term if vocab.get(term) != None else "___UNK___" for term in t.parse(inputs).strip().split(' ')]
        TextList.data = data
        #print(data)
    @staticmethod
    def init_state():
        TextList.state =  make_initial_state(n_units, batchsize=1, train=False)
    @staticmethod
    def process_state():
        buff = []
        for index,term in [(vocab.get(term),term) for term in TextList.data]:
            if index == None:
                #print(term, '0', 'undefined')
                # _ = [ term + ':0'] 
                _ = [ term ] 
                _.extend( ['0:0' for x in range(10)] ) 
                buff.append( _ )
                continue

            char = np.array([index], dtype=np.int32)
            TextList.state, prob = model.forward_one_step(char, char, TextList.state, train=False)
            probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
            probability /= np.sum(probability)
            prob_with_term = []
            for e, p in enumerate(probability):
                prob_with_term.append( [p, ivocab[e] ] )
            prob_with_term = sorted(prob_with_term, key=lambda x:-1 * x[0] )
            if TextList.before_rank == None:
                #print(ivocab[index], "this is head")
                #_ = [ ivocab[index] + ':0.'] 
                _ = [ ivocab[index] ] 
                _.extend( ['0:0' for x in range(10)] ) 
                buff.append( _ )
            else:
                #print(''.join(map(str,[ivocab[index],":",str(math.log(TextList.before_prob[index]))[:5]])), \
                #        [':'.join(map(str, [(lambda x:x if x not in ['', ' ', '　'] else '<space>')(tp[1]), str(math.log(tp[0]))[:5] ] )) for tp in TextList.before_rank[:10]] \
                #        )
                #print(TextList.before_prob[index])
                if TextList.before_prob[index] == 0.:
                    _ = [ ''.join(map(str,["<<", ivocab[index] , ">>"])) ]
                elif math.log(TextList.before_prob[index]) <= -20:
                    _ = [ ''.join(map(str,["<<", ivocab[index] , ">>"])) ]
                else:
                    #_ = [ ''.join(map(str,[ivocab[index] + "",":",str(math.log(TextList.before_prob[index]))[:5]])) ]
                    _ = [ ''.join(map(str,[ivocab[index] + ""])) ]
                _.extend( [':'.join(map(str, [(lambda x:x if x not in ['', ' ', '　'] else '<space>')(tp[1]), str(math.log(tp[0]))[:5] ] )) for tp in TextList.before_rank[:10]] )
                buff.append( _ )
            TextList.before_prob = probability
            TextList.before_rank = prob_with_term
        #print()
        #print( list(map(list, zip(*buff))) )
        inv = list(map(list, zip(*buff))) 
        
        #print('\n'.join([','.join(map(str, iner)) for iner in inv]) )
        print("[proofreading]", [''.join(map(str, iner)) for iner in inv].pop(0) )
        return TextList.state

if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if line == '' or 'http' in line: continue
        TextList.init_state()
        line = line.strip()
        TextList.update_data(line)
        print("[original]", line)
        state = TextList.process_state()


if __name__ == '__test__':
    TextList.init_state()
    TextList.update_data("この情報は初期値なので任意の文字列に入れ替えてください。fuckin hot")
    state = TextList.process_state()
