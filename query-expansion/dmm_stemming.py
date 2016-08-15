# coding: utf-8
import regex
import os
import sys

if '-s' in sys.argv:
    for line in sys.stdin:
        line = line.strip()
        line = regex.sub('【.*?】', '', line)
        line = regex.sub('’', '', line)
        line = regex.sub('‘', '', line)
        line = regex.sub('”', '', line)
        line = regex.sub('(（|）|「|」|『|』)', '', line)
        line = regex.sub('○', '●', line)
        line = regex.sub('(マ|ま)●(コ|こ)', 'マンコ', line)
        line = regex.sub('●ンコ', 'マンコ', line)
        line = regex.sub('ち●ぽ', 'ちんぽ', line)
        line = regex.sub('チ●(ポ|コ)', 'ちんぽ', line)
        line = regex.sub('ロ●', 'ロリ', line)
        line = regex.sub('！{1,}', '!', line)
        line = regex.sub('!{1,}', '!', line)
        line = regex.sub('１', '1', line)
        line = regex.sub('２', '2', line)
        line = regex.sub('３', '3', line)
        line = regex.sub('４', '4', line)
        line = regex.sub('５', '5', line)
        line = regex.sub('６', '6', line)
        line = regex.sub('７', '7', line)
        line = regex.sub('８', '8', line)
        line = regex.sub('９', '9', line)
        line = regex.sub('０', '0', line)
        print line
if '-u' in sys.argv:
    with open('./dmm_wakati_utf8.txt', 'w') as f:
        buff = []
        for line in sys.stdin:
            line = line.strip()
            if 'dummy' in line:
                continue
            try:
                line = line.decode('utf-8')
            except:
                continue
            print line
            f.write(line.encode('utf-8') + '\n' )

