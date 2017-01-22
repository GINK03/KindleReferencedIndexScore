# coding:utf-8
import os
import sys
import subprocess
import argparse
import codecs
import locale
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
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
        print(text)
        res = subprocess.check_output(['python3', 'proofreading.py', '--vocabulary', \
                                                                    './data/' + target + '/vocab.bin', \
                                                                    '--model', 'cv/' + target + '/latest_' + target + '_' + str(rnn_num) + '.chainermodel', \
                                                                    '--primetext', '1', \
                                                                    '--gpu', '-1', \
                                                                    '--length','15', \
                                                                    '--text', text])
        print(res.decode('utf-8'))
        ps_raw = filter(lambda x: 'chosen_ps' in x , str( res ).split('\n'))
        #ps_raw = list(ps_raw).pop().split('=').pop()

