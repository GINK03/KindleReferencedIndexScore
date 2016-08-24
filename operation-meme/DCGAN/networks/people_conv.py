import chainer
import chainer.functions as F
import chainer.links as L

class Generator(chainer.Chain):
	"""docstring for Generator"""
	def __init__(self):
		super(Generator, self).__init__(
			l1=L.Linear(100,128*16*16),
            dcv1=L.Deconvolution2D(in_channels=128,out_channels=64,ksize=4,stride=2,pad=1),
            dcv2=L.Deconvolution2D(in_channels=64,out_channels=1,ksize=4,stride=2,pad=1),
            bc1=L.BatchNormalization(size=128),
            bc2=L.BatchNormalization(size=64))
		self.in_size=100
		self.out_size=1*64*64
		self.imshape=(1,64,64)

	def __call__(self, x, train=True):
		h1 = F.relu(self.bc1(F.reshape(self.l1(x),(x.data.shape[0],128,16,16))))
		h2 = F.relu(self.bc2(self.dcv1(h1)))
		return self.dcv2(h2)

class Discriminator(chainer.Chain):
	"""docstring for Discriminator"""
	def __init__(self):
		super(Discriminator, self).__init__(
            conv1=L.Convolution2D(in_channels=1,out_channels=64,ksize=5,stride=2,pad=2),
            conv2=L.Convolution2D(in_channels=64,out_channels=128,ksize=5,stride=2,pad=2),
            bc1=L.BatchNormalization(size=64),
            bc2=L.BatchNormalization(size=128),
            l1=L.Linear(128*16*16, 1))
		self.in_size = 1*64*64
		self.out_size = 1
		self.imshape=(1,64,64)

	def __call__(self, x, train=True):
		h1 = F.leaky_relu(self.bc1(self.conv1(x)))
		h2 = F.leaky_relu(self.bc2(self.conv2(h1)))
		return self.l1(h2)