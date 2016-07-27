from __future__ import print_function
import sys
import os
import math

class IDFHolder:
    IDFs = {}
    @staticmethod
    def loadFile():
        D = 0
        with open('./stash/idf_base.txt', 'r') as file:
            for line in file.read().split('\n'):
                try:
                    (t, D, dnum, _, allnum) = line.split(' ')
                except ValueError, e:
                    continue
                idf = math.log(float(D)/float(dnum) ) 
                IDFHolder.IDFs.update({t: idf } )
        
        for t,pair in sorted(IDFHolder.IDFs.items(), key=lambda x:x[1]):
            #print(t,pair[0], pair[1])
            pass


IDFHolder.loadFile()
