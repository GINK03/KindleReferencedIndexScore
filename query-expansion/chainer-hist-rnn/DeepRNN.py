# coding: utf-8
import numpy as np
from chainer import Variable, FunctionSet
import chainer.functions as F
import chainer.links as L
import chainer.links.connection.gru as GRU


print("これは、CharRNNを改造したモデルです！メモリの使用量や、GPUのリソースの消費量に差があります!")
class DeepRNN(FunctionSet):
    def __init__(self, n_vocab, n_units):
        super(DeepRNN, self).__init__(
            embed = F.EmbedID(n_vocab, n_units),
            l1_x = L.Linear(n_units, 4*n_units),
            l1_h = L.Linear(n_units, 4*n_units),
            l2_x = L.Linear(n_units, 4*n_units),
            l2_h = L.Linear(n_units, 4*n_units),
            l3_x = L.Linear(n_units, 4*n_units),
            l3_h = L.Linear(n_units, 4*n_units),
            l4   = L.Linear(n_units, n_vocab),
        )
        for param in self.parameters:
            param[:] = np.random.uniform(-0.08, 0.08, param.shape)
    def forward_one_step(self, x_data, y_data, state, train=True, dropout_ratio=0.5):
        x = Variable(x_data, volatile=not train)
        t = Variable(y_data, volatile=not train)
        #print(state)
        h0      = self.embed(x)
        h1_in   = self.l1_x(F.dropout(h0, ratio=dropout_ratio, train=train)) + self.l1_h(state['h1'])
        c1, h1  = F.lstm(state['c1'], h1_in)
        h2_in   = self.l2_x(F.dropout(h1, ratio=dropout_ratio, train=train)) + self.l2_h(state['h2'])
        c2, h2  = F.lstm(state['c2'], h2_in)
        h3_in   = self.l3_x(F.dropout(h2, ratio=dropout_ratio, train=train)) + self.l3_h(state['h3'])
        c3, h3  = F.lstm(state['c3'], h3_in)
        y       = self.l4(F.dropout(h3, ratio=dropout_ratio, train=train))
        state   = {'c1': c1, 'h1': h1, 'c2': c2, 'h2': h2, 'c3':c3, 'h3':h3}
        #print(state)
        if train:
            return state, F.softmax_cross_entropy(y, t)
        else:
            return state, F.softmax(y)
    @staticmethod
    def make_initial_state(n_units, batchsize=50, train=True):
        return {name: Variable(np.zeros((batchsize, n_units), dtype=np.float32),
            volatile=not train)
            for name in ('c1', 'h1', 'c2', 'h2', 'c3', 'h3')}

class MoreDeepRNN(FunctionSet):
    def __init__(self, n_vocab, n_units):
        super(MoreDeepRNN, self).__init__(
            embed = F.EmbedID(n_vocab, n_units),
            l1_x = L.Linear(n_units*2, 4*n_units),
            l1_h = L.Linear(n_units, 4*n_units),
            l2_x = L.Linear(n_units, 4*n_units),
            l2_h = L.Linear(n_units, 4*n_units),
            l3_x = L.Linear(n_units, 4*n_units),
            l3_h = L.Linear(n_units, 4*n_units),
            l4_x = L.Linear(n_units, 4*n_units),
            l4_h = L.Linear(n_units, 4*n_units),
            l5   = L.Linear(n_units, n_vocab),
        )
        for param in self.parameters:
            param[:] = np.random.uniform(-0.08, 0.08, param.shape)
    def forward_one_step(self, x_data, y_data, state, train=True, dropout_ratio=0.5):
        x = Variable(x_data, volatile=not train)
        t = Variable(y_data, volatile=not train)
        # 実際に評価する際には、必須となるヒント情報が必要であるので、x_data[:,1~]以降はメタ情報になっている
        t_head = y_data[:,0]
        h0      = self.embed(x)
        h1_in   = self.l1_x(F.dropout(h0, ratio=dropout_ratio, train=train)) + self.l1_h(state['h1'])
        c1, h1  = F.lstm(state['c1'], h1_in)
        h2_in   = self.l2_x(F.dropout(h1, ratio=dropout_ratio, train=train)) + self.l2_h(state['h2'])
        c2, h2  = F.lstm(state['c2'], h2_in)
        h3_in   = self.l3_x(F.dropout(h2, ratio=dropout_ratio, train=train)) + self.l3_h(state['h3'])
        c3, h3  = F.lstm(state['c3'], h3_in)
        h4_in   = self.l4_x(F.dropout(h3, ratio=dropout_ratio, train=train)) + self.l4_h(state['h4'])
        c4, h4  = F.lstm(state['c4'], h4_in)
        y       = self.l5(F.dropout(h4, ratio=dropout_ratio, train=train))
        state   = {'c1': c1, 'h1': h1, 'c2': c2, 'h2': h2, 'c3':c3, 'h3':h3, 'c4':c4, 'h4': h4}
        if train:
            #return state, F.softmax_cross_entropy(y, t)
            return state, F.softmax_cross_entropy(y, t_head)
        else:
            return state, F.softmax(y)
    @staticmethod
    def make_initial_state(n_units, batchsize, train=True):
        return {name: Variable(np.zeros((batchsize, n_units), dtype=np.float32),
            volatile=not train)
            for name in ('c1', 'h1', 'c2', 'h2', 'c3', 'h3', 'c4', 'h4')}
