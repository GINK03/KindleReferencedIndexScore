
import os
import math
import typing

s = input()
cnv = str(bin(int(s.replace('hamu', '1').replace('ham', '0'), 2)*2))
print(cnv.replace('0b', '').replace('1', 'hamu').replace('0', 'ham'))
