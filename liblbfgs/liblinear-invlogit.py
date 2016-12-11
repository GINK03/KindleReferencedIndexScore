# coding: utf-8
from __future__ import print_function
import os
import sys
import math
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import fmin_l_bfgs_b
import scipy
import pandas as pd
import numpy as np
from sklearn import linear_model
import sklearn
import sklearn.datasets 
clf = linear_model.LinearRegression()

if __name__ == '__test__':
    wine = pd.read_csv("winequality-red.csv", sep=";")
    #print(wine.head)
    # 説明変数に "density (濃度)" を利用
    X = wine.loc[:, ['density', 'pH']].as_matrix()
    # 目的変数に "alcohol (アルコール度数)" を利用
    Y = wine['alcohol'].as_matrix()
    # 予測モデルを作成
    clf.fit(X, Y)
    # 回帰係数
    print(clf.coef_)
    # 切片 (誤差)
    print(clf.intercept_)
    # 決定係数
    print(clf.score(X, Y))

    # 説明変数に "density (濃度)" を利用
    X = wine.ix[:, [7, 8]]
    # 目的変数に "alcohol (アルコール度数)" を利用
    Y = wine.ix[:, [10]]
    # 予測モデルを作成
    clf.fit(X, Y)
    # 回帰係数
    print(clf.coef_)
    # 切片 (誤差)
    print(clf.intercept_)
    # 決定係数
    print(clf.score(X, Y))
    #print(Y)
    print(X)


if __name__ == '__main__':
    from scipy import linalg as LA
    if '--sample' in sys.argv: 
       ctr = sklearn.datasets.load_svmlight_file('./akatsuki.tokitsukaze.head250000.txt')
    else:
       fname = filter(lambda x:'-f=' in x, sys.argv).pop().split('=').pop()
       ctr = sklearn.datasets.load_svmlight_file(fname)
    
    X = ctr[0]
    Y_raw = pd.DataFrame(ctr[1])
    import math
    Y = [0.0]*len(Y_raw)
    for i in range(len(ctr[1])):
            Y[i] = -1. * math.log(1./ctr[1][i] - 1.)

    Y = pd.DataFrame(Y)
    clf.fit(X, Y)
    #print("回帰係数", ','.join(map(str, list(clf.coef_[0]))) )
    # 切片 (誤差)
    print("切片", clf.intercept_)
    # 決定係数
    print("決定係数", clf.score(X, Y))
    result = ["回帰係数", ','.join(map(str, list(clf.coef_[0]))), "切片", clf.intercept_, "決定係数", clf.score(X, Y)]
    file('result.txt', 'w').write('\n'.join(map(str, result)))
