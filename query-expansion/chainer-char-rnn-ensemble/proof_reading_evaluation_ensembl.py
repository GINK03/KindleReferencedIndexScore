# coding:utf-8
import os
import sys
import subprocess
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rnn_num', type=int, default=128)
    parser.add_argument('--target',  type=str, default='piconews')
    parser.add_argument('--modeltype',  type=str, default='dummy')
    args = parser.parse_args()
    rnn_num = args.rnn_num
    target  = args.target
    modeltype = args.modeltype 
    if modeltype == 'none':
        modeltype = ''
    print  'I will use model of cv/latest_' + modeltype + '_' + str(rnn_num) + '.chainermodel'
    for i, line in enumerate(sys.stdin):
        line = line.strip()
    
        text = line
        res = subprocess.check_output(['python', 'proofreading_ensembl.py', \
                                                                    \
                                                                    '--primetext', '1', \
                                                                    '--gpu', '-1', \
                                                                    '--length','15', \
                                                                    '--text', text])
        #print(res)
        print res
        ps_raw = filter(lambda x: 'ensembl_ps' in x , res.split('\n'))
        ps_raw = ps_raw.pop().split('=').pop().strip()
        import json
        ps = json.loads(ps_raw)
        print i, ',', sum([sum(p)/len(p) for p in ps])/len(ps)


