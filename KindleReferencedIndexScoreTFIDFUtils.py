from __future__ import print_function
import sys
import os
import math

class IDFHolder:
    IDFs = {}
    @staticmethod
    def loadFile(inputpath):
        D = 0
        with open(inputpath, 'r') as file:
            for line in file.read().split('\n'):
                try:
                  (t, D, dnum, _, allnum, asins) = line.split('___')
                  D     = float(D)
                  dnum  = float(dnum) 
                except:
                  print(line)
                  continue
                idf = math.log(float(D)/float(dnum) ) 
                IDFHolder.IDFs.update({t: idf } )
        
        for t,idf in sorted(IDFHolder.IDFs.items(), key=lambda x:x[1]):
            print(t, idf)
            pass
if __name__ == '__main__':
  IDFHolder.loadFile(sys.argv[1])
