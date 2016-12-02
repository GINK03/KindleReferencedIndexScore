# coding: utf-8
import os
import math
import re

class LinearRegresser:
    def __init__(self, fname):
        """
        モデルを読み込んで内部に辞書を構築
        """
        ents = filter(lambda x:'' != x, open(fname).read().split('\n'))
        self.reali_w = {}
        for i, ent in enumerate(ents[6:]):
            real_i, ent = i+1, ent
            self.reali_w[real_i] = float(ent)
    def file_eval(self, fname):
        for line in open(fname).read().split('\n'):
            if line == '' : continue
            tp = filter(lambda x:x != '', line.split(' '))
            real = tp.pop(0)
            score = 0.
            for pair in tp:
                index, weight = pair.split(':')
                index, weight = int(index), float(weight)
                if self.reali_w.get(index) != None:
                    score += self.reali_w[index]*weight
            pred = 1. / ( 1. + math.pow(math.e, score*-1) )
            #print 'prob', real, pred
            print real, '0:' + str(pred) + ' ' + ' '.join(tp)

if __name__ == '__main__':
    lr = LinearRegresser('./train.txt.model')
    lr.file_eval('./train.txt')

