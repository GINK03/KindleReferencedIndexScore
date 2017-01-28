
import os
import math
import sys
import decimal as d
from decimal import Decimal as D
from pprint import pprint
d.getcontext().prec = 1024
Dec = D
Pow = D.__pow__
Mul = D.__mul__
Add = D.__add__

if '--leibniz' in sys.argv:
    def each(n: Dec) -> Dec:
        return Pow(D(-1), n)/Add(Mul(D(2), n), D(1))
    pi_div_4 = Dec(0)
    for n in range(100000):
        pi_div_4 = Add(pi_div_4, each(Dec(n)))
    print("ANS", Mul(D(4), pi_div_4))

