import chainer
import numpy as np
import chainer.functions as F
import chainer.links as L
from chainer import optimizers
from chainer import Variable
from chainer import serializers

class Generator(chainer.Chain):
	"""docstring for Generator"""
	def __init__(self):
		super(Generator, self).__init__(
			l1=L.Linear(100, 100),
			l2=L.Linear(100, 100),
			l3=L.Linear(100, 28*28))
		self.in_size = 100
		self.out_size = 28*28
		self.imshape = (1,28,28)

	def __call__(self, x, train=True):
		h1 = F.relu(self.l1(x))
		h2 = F.relu(self.l2(h1))
		if train:
			h2 = F.dropout(h2)
		return F.tanh(self.l3(h2))

class Discriminator(chainer.Chain):
	"""docstring for Discriminator"""
	def __init__(self):
		super(Discriminator, self).__init__(
            l1=L.Linear(28*28, 100),
            l2=L.Linear(100, 100),
            l3=L.Linear(100, 1))
		self.in_size = 28*28
		self.out_size = 1
		self.imshape = (1,28,28)

	def __call__(self, x, train=True):
		if x.data.shape!=(True,28*28):
			x = chainer.functions.reshape(x,(x.data.shape[0],28*28))
		h1 = F.relu(self.l1(x))
		h2 = F.relu(self.l2(h1))
		if train:
			h2 = F.dropout(h2)
		return F.tanh(self.l3(h2))