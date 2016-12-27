
import os 
import math
import sys
import glob

allname = [fname  for fname in glob.glob('./gp/*')]
orgs = list(filter(lambda x:'.org.' in x, allname))

headers = []
for org in orgs:
  header = '.'.join(org.split('.')[1:5]).split('/').pop()
  headers.append(header)

sliced = headers[0:1000]

for header in sliced:
    os.system('cp ./gp/' + header + '.org.jpg mingp/')
    os.system('cp ./gp/' + header + '.cnv.jpg mingp/')
