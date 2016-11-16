# coding:utf-8
import os
import sys
import subprocess
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rnn_num', type=int, default=128)
    parser.add_argument('--target',  type=str, default='piconews')
    args = parser.parse_args()
    rnn_num = args.rnn_num
    target  = args.target

    for i, line in enumerate(sys.stdin):
        line = line.strip()
    
        text = line
        res = subprocess.check_output(['python', 'proofreading.py', '--vocabulary', \
                                                                    './data/' + target + '/vocab.bin', \
                                                                    '--model', 'cv/latest_' + str(rnn_num) + '.chainermodel', \
                                                                    '--primetext', '1', \
                                                                    '--gpu', '-1', \
                                                                    '--length','15', \
                                                                    '--text', text])
        #print(res)
        ps_raw = filter(lambda x: 'chosen_ps' in x , res.split('\n'))
        ps_raw = ps_raw.pop().split('=').pop()
        ps = map(float, ps_raw.strip().split(' ') )
        print i, ",", sum(ps)/len(ps)

