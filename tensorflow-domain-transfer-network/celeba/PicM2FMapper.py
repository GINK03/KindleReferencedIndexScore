import os
import math
import numpy as np
import glob
import re
import pickle
from PIL import Image
import time
lists = [text for text in filter(lambda x:x!='', open('./list_attr_celeba.txt').read().split('\n'))]
head = lists[1].lower().split()
female_param = {}
male_param   = {}
maxlen = len(lists)
anker_time = time.time()
for i, text in enumerate(lists[2:]):
  name_ents = re.sub('\s{1,}', ' ', text).split()
  name      = name_ents.pop(0)
  ents      = name_ents
  param     = dict(zip(head, ents))
  img = Image.open('./img_align_celeba/%s'%name )
  small = img.resize((32, 32))
  if param['male'] == '-1':
    target = "./female/%s"%(name)
    small.save(target, 'JPEG')
    female_param[name]  = dict(map(lambda x:(x[0], 1) if x[1] == '1' else (x[0], 0), sorted(param.items())))
  else:
    target = "./male/%s"%(name)
    small.save(target, 'JPEG')
    male_param[name]  = dict(map(lambda x:(x[0], 1) if x[1] == '1' else (x[0], 0), sorted(param.items())))
  if i%5000 == 0:
     print("%d/%d"%(i, maxlen), int(time.time() - anker_time))
     anker_time = time.time()

open('female_param.pkl', 'bw').write(pickle.dumps(female_param))
open('male_param.pkl', 'bw').write(pickle.dumps(male_param))
  
