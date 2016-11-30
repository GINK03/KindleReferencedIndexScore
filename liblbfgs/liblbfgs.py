# coding: utf-8
import os
import sys
import math
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import fmin_l_bfgs_b
import scipy
x_ = np.arange(0,10,0.1)
m_ = 0
b_ = 1.0
y_ = m_*x_ + b_

def func(ps, *xs):
    x = xs[0]
    y = xs[1]
    p1, p2 = ps
    error = [p1**2 + p2**2]
    return sum(error)

inits = np.array([1.0, 0.0])
bounds = [(None,200), (None,None)]

result = scipy.optimize.fmin_l_bfgs_b(func, x0=inits, args=(x_, y_), bounds=bounds, approx_grad=True)
print result
