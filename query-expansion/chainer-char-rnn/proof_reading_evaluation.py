# coding:utf-8
import os
import sys
import subprocess

if __name__ == '__main__':
    text = "なかなか上手に仕上げるのが難しいアイロンがけ。どうすれば簡単に、なおかつきれいに仕上げることができるのでしょうか。今回はアイロンがけの基本のやり方や、ワイシャツをきれいに仕上げる方法、時短にもなる便利なアイロングッズなどをご紹介します。アイロンがけのやり方なんて学校で習うわけではないので見よう見まね、という方も多いのではないでしょうか。ここではそんなアイロンがけの基本的なポイントについて解説します。"
    print subprocess.check_output(['python', 'proofreading.py', '--vocabulary', './data/nanoproduction/vocab.bin', '--model', 'cv/latest_512.chainermodel', '--primetext', '1', '--gpu', '-1', '--length','15', '--text', text])

