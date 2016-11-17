# coding: utf-8

import os
import math
import sys
import itertools

if __name__ == '__main__':
    term_freq = {}
    all_term = []
    for line in sys.stdin:
        line = line.strip()
        terms = line.split(' ')
        all_term.extend(terms)
        all_term.append('\n')
        for term in terms:
            if term_freq.get(term) != None:
                term_freq[term] += 1
            else:
                term_freq[term] = 1
    
    th_num_raw = filter(lambda x:'--th_num=' in x , sys.argv)
    th_num = 3000
    if th_num_raw != []:
      th_num = int(th_num_raw.pop().split('=').pop())
    term_freq_th = {}
    for e, (k, v) in enumerate(sorted(term_freq.iteritems(), key=lambda x:x[1]*-1)):
        if e > th_num:
            break
        #print k, v, e
        term_freq_th[k] = v

    for target_term in all_term:
        if term_freq_th.get(target_term) != None or target_term == '\n':
            print target_term,
        else:
            print 'UNK',
