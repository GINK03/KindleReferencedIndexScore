# coding: utf-8
from __future__ import print_function
import pandas as pd
import numpy as np
import tflearn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.client import device_lib

local_device_protos = device_lib.list_local_devices()
print(local_device_protos)

import sys
df = pd.read_csv('./international-airline-passengers.csv', \
	engine='python', \
	usecols=[1], \
	skipfooter=3)
dataset = df.values
dataset = dataset.astype('float32')

contents = filter(lambda x:x!='', open('./international-airline-passengers.csv').read().split('\n'))
dataset = [ [float(i.split(',')[1])] for i in contents ]
dataset = np.array(dataset).astype('float32')


""" ノーマライゼーション """
dataset -= np.min(np.abs(dataset))
dataset /= np.max(np.abs(dataset))
DELTA = 1
def create_dataset(dataset, steps_of_history, steps_in_future):
    X, Y = [], []
    for i in range(0, dataset.size-steps_of_history - DELTA, steps_in_future):
          X.append(dataset[i:i+steps_of_history])
          #Y.append(dataset[i + steps_of_history ])
          Y.append(dataset[i + steps_of_history + DELTA])
    X = np.reshape(np.array(X), [-1, steps_of_history, 1])
    Y = np.reshape(np.array(Y), [-1, 1])
    return X, Y

def split_data(x, y, test_size=0.1):
    pos = round(len(x) * (1 - test_size))
    trainX, trainY = x[:pos], y[:pos]
    testX, testY   = x[pos:], y[pos:]
    return trainX, trainY, testX, testY

steps_of_history = 1
steps_in_future = 1

X, Y = create_dataset(dataset, steps_of_history, steps_in_future)
trainX, trainY, testX, testY = split_data(X, Y, 0.33)
print(X)
net = tflearn.input_data(shape=[None, steps_of_history, 1])
#net = tflearn.lstm(net, n_units=6)
#net = tflearn.gru(net, n_units=6, return_seq=True)
#net = tflearn.gru(net, n_units=6, return_seq=True)
net = tflearn.gru(net, n_units=6)

net = tflearn.fully_connected(net, 1, activation='linear')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
        loss='mean_square')

model = tflearn.DNN(net, tensorboard_verbose=0)

with tf.device('/cpu:0'):
  model.fit(trainX, trainY, validation_set=0.1, batch_size=1, n_epoch=50)


train_predict = model.predict(trainX)
test_predict = model.predict(testX)


train_predict_plot = np.empty_like(dataset)
train_predict_plot[:, :] = np.nan
train_predict_plot[steps_of_history:len(train_predict)+steps_of_history, :] = train_predict

test_predict_plot = np.empty_like(dataset)
test_predict_plot[:, :] = np.nan
test_predict_plot[len(train_predict)+steps_of_history:len(dataset) - DELTA , :] = test_predict

plt.figure(figsize=(8, 8))
plt.title('History={} Future={}'.format(steps_of_history, steps_in_future))
plt.plot(dataset)
plt.plot(train_predict_plot)
plt.plot(test_predict_plot)
plt.savefig('passenger.png')
#print(train_predict_plot)

