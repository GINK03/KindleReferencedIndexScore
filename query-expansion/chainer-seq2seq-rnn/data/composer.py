import os
import sys
import math
import MeCab
import re
t = MeCab.Tagger('-Owakati')
t_chasen =  MeCab.Tagger('-Ochasen')

if '--term' in sys.argv:
  for line in open('./eijiro.txt').read().split('\n'):
    st = line.split('◆')
    head = st[0]
    mini = head.split(':')
    eng = mini[0]
    eng_converted = re.sub('\s{1,}', ' ', eng.lower())
    jap = ' '.join(mini[1:])
    jap_parse = re.sub('\s{1,}', ' ', t.parse(jap).replace('\n', ''))
    print(' '.join([eng_converted, '<D>', jap_parse, '<EOS>']))

if '--char' in sys.argv:
  for line in open('./eijiro.txt').read().split('\n'):
    st = line.split('◆')
    head = st[0]
    mini = head.split(':')
    eng = mini[0]
    eng_converted = re.sub('\s{1,}', ' ', '_'.join(list(eng.lower())))
    jap = ' '.join(mini[1:])
    jap_parse = re.sub('\s{1,}', ' ', '_'.join(list(jap.replace('\n', '')) ) )
    print(' '.join([eng_converted, 'D', jap_parse, 'E']))

if '--katakana' in sys.argv:
  KATAKANA = set(list("""アイウエオ
ァィゥェォ
カキクケコ
ガギグゲゴ
サシスセソ
ザジズゼゾ
タチツテト
ダヂヅデド
ナニヌネノ
ハヒフヘホ
バビブベボ
パピプペポ
マミムメモ
ヤユヨ
ラリルレロ
ワオン
。「」、
""".replace('\n','') ) )
  ALPHABET = set(list("""abcdefghijklmnopqrstuvwxyz.\" """))
  for line in open('./eijiro.txt').read().split('\n'):
    st = line.split('◆')
    head = st[0]
    mini = head.split(':')
    eng = mini[0]
    eng_converted = re.sub('\s{1,}', ' ', ''.join(filter(lambda x: x in  ALPHABET, list(eng.lower()))))
    jap = ' '.join(mini[1:])
    katakana = ''.join(map(lambda x:x[1], \
                    filter(lambda x:len(x) > 2, \
                    [line.split('\t') for line in  t_chasen.parse(jap).split('\n')] \
                    ) \
                ) \
            )
    filtered = ''.join(filter(lambda x:x in KATAKANA, list(katakana) ))
    jap_parse = re.sub('\s{1,}', ' ', filtered)
    #print(eng_converted)
    #print(jap_parse)
    print(' '.join([eng_converted, 'D', jap_parse, 'E']))
