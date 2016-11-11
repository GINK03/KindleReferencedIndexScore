# coding:utf-8
import os
import sys
import subprocess

if __name__ == '__main__':
    for i, line in enumerate(sys.stdin):
        line = line.strip()
        text = line
        res = subprocess.check_output(['python', 'proofreading.py', '--vocabulary', './data/nanoproduction/vocab.bin', '--model', 'cv/latest_512.chainermodel', '--primetext', '1', '--gpu', '-1', '--length','15', '--text', text])
        print res
        ps_raw = filter(lambda x: 'chosen_ps' in x , res.split('\n'))
        print i, ps_raw.pop()

