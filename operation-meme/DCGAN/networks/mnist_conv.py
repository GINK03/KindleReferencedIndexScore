import chainer
import chainer.functions as F
import chainer.links as L

class Generator(chainer.Chain):
	"""docstring for Generator"""
	def __init__(self):
		super(Generator, self).__init__(
			l1=L.Linear(100,50*5*5),
            dcv1=L.Deconvolution2D(in_channels=50,out_channels=10,ksize=3,stride=3),
            dcv2=L.Deconvolution2D(in_channels=10,out_channels=1,ksize=2,stride=2,pad=1),
            bc1=L.BatchNormalization(size=50),
            bc2=L.BatchNormalization(size=10))
		self.in_size=100
		self.imshape=(1,28,28)

	def __call__(self, x, train=True):
		h1 = F.leaky_relu(self.bc1(F.reshape(self.l1(x),(x.data.shape[0],50,5,5))))
		h2 = F.leaky_relu(self.bc2(self.dcv1(h1)))
		return F.sigmoid(self.dcv2(h2))

class Discriminator(chainer.Chain):
	"""docstring for Discriminator"""
	def __init__(self):
		super(Discriminator, self).__init__(
            conv1=L.Convolution2D(in_channels=1,out_channels=10,ksize=5,stride=2,pad=2),
            conv2=L.Convolution2D(in_channels=10,out_channels=50,ksize=3,stride=1,pad=0),
            bc1=L.BatchNormalization(size=10),
            bc2=L.BatchNormalization(size=50),
            l1=L.Linear(4*4*50, 1))
		self.in_size = (1,28,28)
		self.out_size = 1
		self.imshape=(1,28,28)

	def __call__(self, x, train=True):
		h1 = F.max_pooling_2d(self.bc1(self.conv1(x)),4,stride=2)
		h2 = F.relu(self.bc2(self.conv2(h1)))
		if train:
			h2 = F.dropout(h2)
		return F.sigmoid(self.l1(h2))