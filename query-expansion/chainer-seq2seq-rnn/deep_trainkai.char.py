# coding: utf-8
import time
import math
import sys
import argparse
import pickle as pickle
import copy
import os
import codecs

import numpy as np
from chainer import cuda, Variable, FunctionSet, optimizers
import chainer.functions as F
if '--moreDeep' in sys.argv:
   from DeepRNN import MoreDeepRNN as DeepRNN
else:
   from DeepRNN import DeepRNN as DeepRNN

make_initial_state = DeepRNN.make_initial_state

def load_data(args):
    print('%s'%(args.data_dir))
    words = ''
    line = ''
    raw = open('%s/input.txt' %(args.data_dir), 'r').read().replace('\n', '')
    vocab = {}
    sentences = [x.split('_') for x in raw.split('<EOS>')]
    term_set = set()
    for _ in sentences:
        for __ in _:
            term_set.add(__)
    for i, term in enumerate(term_set):
        vocab[term] = i
    maxlen     = max( [len(x) for x in sentences] )
    dataset = []
    for i, sentence in enumerate(sentences):
        if len(sentence) > 101:
            continue
        tag = [0]*101 
        #[vocab[term] for j, word in enumerate(sentence)]
        for j, word in enumerate(sentence):
            if j >= 101: break
            #print(sentence)
            tag[j] = vocab[word]
        dataset.append(np.array(tag, dtype='int32'))
        #print('iter')

    print('corpus length:', len(sentences)*100)
    print('vocab size:', len(vocab))
    return dataset, words, vocab

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('--data_dir',                   type=str,   default='data/tinyshakespeare')
parser.add_argument('--checkpoint_dir',             type=str,   default='')
parser.add_argument('--json',                       type=str,   default='1.json')
parser.add_argument('--gpu',                        type=int,   default=-1)
parser.add_argument('--rnn_size',                   type=int,   default=768)
parser.add_argument('--learning_rate',              type=float, default=2e-3)
parser.add_argument('--learning_rate_decay',        type=float, default=0.97)
parser.add_argument('--learning_rate_decay_after',  type=int,   default=10)
parser.add_argument('--decay_rate',                 type=float, default=0.95)
parser.add_argument('--dropout',                    type=float, default=0.0)
parser.add_argument('--seq_length',                 type=int,   default=50)
parser.add_argument('--batchsize',                  type=int,   default=100)
parser.add_argument('--epochs',                     type=int,   default=50)
parser.add_argument('--grad_clip',                  type=int,   default=5)
parser.add_argument('--init_from',                  type=str,   default='')

args = parser.parse_args()

if args.checkpoint_dir == '':
    args.checkpoint_dir = args.data_dir
if not os.path.exists(args.checkpoint_dir):
    os.mkdir(args.checkpoint_dir)

n_epochs    = args.epochs
n_units     = args.rnn_size
batchsize   = args.batchsize
bprop_len   = args.seq_length
grad_clip   = args.grad_clip

train_data, words, vocab = load_data(args)
pickle.dump(vocab, open('%s/vocab.bin'%(args.data_dir), 'wb'))
filename = args.data_dir.split('/')[1]
print('I will save a file name contains ', filename)

if len(args.init_from) > 0:
    model = pickle.load(open(args.init_from, 'rb'))
else:
    model = DeepRNN(len(vocab), n_units)

if args.gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()

optimizer = optimizers.RMSprop(lr=args.learning_rate, alpha=args.decay_rate, eps=1e-8)
optimizer.setup(model)

#whole_len    = train_data.shape[0]
#jump         = whole_len / batchsize
epoch        = 0
start_at     = time.time()
cur_at       = start_at
state        = make_initial_state(n_units, batchsize=batchsize)
if args.gpu >= 0:
    accum_loss   = Variable(cuda.zeros(()))
    for key, value in list(state.items()):
        value.data = cuda.to_gpu(value.data)
else:
    accum_loss   = Variable(np.zeros((), dtype=np.float32))

#print('going to train {} iterations'.format(ump * n_epochs))
loss_rate = 0.0
size = len(train_data)
for i in range(size * n_epochs):
    x_batch = train_data[i%size][:-1]
    y_batch = train_data[i%size][1:]
    #print(len(x_batch))
    if args.gpu >=0:
        x_batch = cuda.to_gpu(x_batch)
        y_batch = cuda.to_gpu(y_batch)

    state, loss_i = model.forward_one_step(x_batch, y_batch, state, dropout_ratio=args.dropout)
    accum_loss   += loss_i

    if (i + 1) % bprop_len == 0:  # Run truncated BPTT
        now = time.time()
        print('{}/{}, train_loss = {}, time = {:.2f}'.format((i+1)/bprop_len, size * n_epochs, accum_loss.data / bprop_len, now-cur_at))
        loss_rate = accum_loss.data / bprop_len
        cur_at = now
        optimizer.zero_grads()
        accum_loss.backward()
        accum_loss.unchain_backward()  # truncate
        if args.gpu >= 0:
            accum_loss = Variable(cuda.zeros(()))
        else:
            accum_loss = Variable(np.zeros((), dtype=np.float32))
        optimizer.clip_grads(grad_clip)
        optimizer.update()
    if (i + 1) % 5000 == 0:
        print(' will save chainermodel data...')
        print( '%s/latest_deeprnn_%s_%s_%d.chainermodel'%(args.checkpoint_dir, filename, args.json, n_units) )
        copyed_obj = copy.deepcopy(model).to_cpu()
        pickle.dump(copyed_obj, open('%s/latest_deeprnn_%s_%s_%d.chainermodel'%(args.checkpoint_dir, filename, args.json, n_units), 'wb'))

    if (i + 1) % 100 == 0:
        epoch += 1
        if epoch >= args.learning_rate_decay_after:
            optimizer.lr *= args.learning_rate_decay
            print('decayed learning rate by a factor {} to {}'.format(args.learning_rate_decay, optimizer.lr))

    sys.stdout.flush()
pickle.dump(copy.deepcopy(model).to_cpu(), open('%s/finished_deeprnn_%s_%s_%d.chainermodel'%(args.checkpoint_dir, filename, args.json, n_units), 'wb'))
