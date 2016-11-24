# coding: utf-8
import os
import sys
import math
from sklearn.ensemble import RandomForestClassifier


if '--example' in sys.argv:
    trainingdata = [[1, 1], [2, 0.5], [-1, -1], [-2, -2]]
    traininglabel = [1, 1, -1, -1]
    testdata = [[1, 3], [-3, -3]]
    model = RandomForestClassifier()
    model.fit(trainingdata, traininglabel)
    output = model.predict(testdata)
    for label in output: 
        print label
    probas = model.predict_proba(testdata)
    for label in probas:
        print label
    for weights in model.get_params():
        print weights
    for i, gini_imp in enumerate(model.feature_importances_):
        print "gini係数 index = ", i, gini_imp


if '--learn' in sys.argv:
    import json
    anses = []
    traings = []
    for line in open('./learning.json').read().split('\n'):
        if line.strip() == "" : continue
        ans_label, data = json.loads(line.strip())
        anses.append(ans_label)
        traings.append(data)
    model = RandomForestClassifier()
    model.fit(traings, anses)
    import pickle

    open('rf_proofreading.model', 'w').write(pickle.dumps(model))

if '--eval' in sys.argv:
    import json
    import pickle
    model = pickle.loads(open('rf_proofreading.model').read())
    anses = []
    tests = []
    for line in open('eval.json').read().split('\n'):
        if line.strip() == "" : continue
        ans_label, data = json.loads(line.strip())
        anses.append(ans_label)
        tests.append(data)
        
    output = model.predict(tests)
    total = 0
    acc   = 0
    for real, pred in zip(anses, output):
        print real, pred
        if real == pred:
            acc += 1
        total += 1
    print acc / float(total)
