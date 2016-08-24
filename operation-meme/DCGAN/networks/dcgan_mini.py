import chainer
import chainer.functions as F
import chainer.links as L

class Generator(chainer.Chain):
	"""docstring for Generator"""
	def __init__(self):
		super(Generator, self).__init__(
			l1=L.Linear(100,512*4*4),
            dcv1=L.Deconvolution2D(in_channels=512,out_channels=256,ksize=4,stride=2,pad=1),
            dcv2=L.Deconvolution2D(in_channels=256,out_channels=128,ksize=4,stride=2,pad=1),
            dcv3=L.Deconvolution2D(in_channels=128,out_channels=3,ksize=4,stride=2,pad=1),
            bc1=L.BatchNormalization(size=512),
            bc2=L.BatchNormalization(size=256),
            bc3=L.BatchNormalization(size=128))
		self.in_size=100
		self.out_size=3*64*64
		self.imshape=(3,64,64)

	def __call__(self, x, train=True):
		h1 = F.relu(self.bc1(F.reshape(self.l1(x),(x.data.shape[0],512,4,4))))
		h2 = F.relu(self.bc2(self.dcv1(h1)))
		h3 = F.relu(self.bc3(self.dcv2(h2)))
		return self.dcv3(h3)

class Discriminator(chainer.Chain):
	"""docstring for Discriminator"""
	def __init__(self):
		super(Discriminator, self).__init__(
            conv1=L.Convolution2D(in_channels=3,out_channels=128,ksize=5,stride=2,pad=2),
            conv2=L.Convolution2D(in_channels=128,out_channels=256,ksize=5,stride=2,pad=2),
            conv3=L.Convolution2D(in_channels=256,out_channels=512,ksize=5,stride=2,pad=2),
            bc1=L.BatchNormalization(size=128),
            bc2=L.BatchNormalization(size=256),
            bc3=L.BatchNormalization(size=512),
            l1=L.Linear(4*4*512, 1))
		self.in_size = 3*64*64
		self.out_size = 1
		self.imshape=(3,64,64)

	def __call__(self, x, train=True):
		h1 = F.leaky_relu(self.bc1(self.conv1(x)))
		h2 = F.leaky_relu(self.bc2(self.conv2(h1)))
		h3 = F.leaky_relu(self.bc3(self.conv3(h2)))
		return self.l1(h3)