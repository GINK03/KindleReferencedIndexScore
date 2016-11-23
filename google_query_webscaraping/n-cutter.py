
import sys
import os
import math

idf = {}
maxx = 0
hozon = []
for i, line in enumerate(sys.stdin):
    maxx += 1
    hozon.append(line)
    for t in set(line.split(" ")):
        if idf.get(t) == None:
            idf[t] = 1
        else:
            idf[t] += 1

idflog = {}
for t, n in idf.iteritems():
    """処理できる計算結果より、idfが4以下のみ保存する """
    if int( math.log( maxx/float(idf[t]) ) ) <= 4:
        idflog[t] = math.log( maxx/float(idf[t]) )

for line in hozon:
    for t in line.split(" "):
        if idflog.get(t) != None:
            print t, 
        else:
            print "mask"
    print

if "-c" in sys.argv:
    for t, n in filter(lambda x:x[1] == 3, idf.iteritems()):
        print t, n

if "--hist" in sys.argv:
    invidf = {}
    for t, f in idflog.iteritems():
        if invidf.get(int(f)) == None:
            invidf[int(f)] = 1
        else:
            invidf[int(f)] += 1
    for i, hist in sorted(invidf.iteritems(), key=lambda x:x[1]):
        print i, hist


