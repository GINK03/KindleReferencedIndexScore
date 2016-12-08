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

it = 1
def func(ps, *xs):
    global it
    error = 0.
    it += 1
    for contain in container:
        target = contain[0]
        buff = 0.
        feats  = contain[1]
        for i in range(max_f):
           if feats.get(i) != None:
             buff += feats[i]*ps[i]
        buff += ps[max_f]
        error += buff - 1. / (1. + math.pow(math.e, buff*-1) )
    if it % 10 == 0:
        print 'iter ', it, 'error rate', error, 'buff', buff
    return error

filenames = filter(lambda x:'-f=' in x, sys.argv)
filename = ''
if filenames != []:
    filename = filenames.pop().split('=').pop()

modelnames = filter(lambda x:'-m=' in x, sys.argv)
modelname = ''
if modelnames != []:
    modelname = modelnames.pop().split('=').pop()

if 'train' in sys.argv:
    max_f = 0
    for line in open(filename).read().split('\n'):
        if line == '': continue
        tp = line.split(' ')
        tp.pop(0)
        max_f = max(max_f, max( map(lambda x:int(x.split(':').pop(0)), tp) ) )

    max_f += 1
    #print max_f
    inits = np.array([0.0]*(max_f+1))
    bounds = []
    for _ in range(max_f+1):
        bounds.append( (-1.,1.) )

    from collections import Counter
    container = []
    for line in open(filename).read().split('\n'):
        if line == '': continue
        tp = line.split(' ')
        t = float(tp.pop(0))
        c = dict(map(lambda x: (int(x.split(':')[0]), float(x.split(':')[1])), tp) )
        container.append( (t, c) )

    result = scipy.optimize.fmin_l_bfgs_b(func, x0=inits, args=(x_, y_), bounds=bounds, approx_grad=True)
    #result = scipy.optimize.minimize(func, x0=inits, args=(x_, y_), )
    print 'result', result
    model = result[0]
    print 'model', ', '.join(map(str, list(model)))
    import json
    open(filename + '.model', 'w').write(json.dumps(list(model)))

if 'pred' in sys.argv:
    import json
    model = json.loads(open(modelname).read())
    for line in open(filename).read().split('\n'):
        if line == '' : continue
        tp = line.split(' ')
        target = float(tp.pop(0))
        c = dict(map(lambda x: (int(x.split(':')[0]), float(x.split(':')[1])), tp) )
        pred = 0.
        for index, b in c.items():
           pred += b*model[index]
        pred += model[-1]
        print target, 'pred', pred, 'real', target, 'delta**2', (target - pred)**2
         
