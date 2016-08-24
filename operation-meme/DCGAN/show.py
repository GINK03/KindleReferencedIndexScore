import numpy as np
from chainer import Variable
from chainer import serializers
import sys
sys.path.append('./networks')

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output_dir','-o',default = None)
parser.add_argument('--input_file','-i',default = None, help = 'Path to h5 file')
parser.add_argument('--mode','-m',help = 'Train mode (mnist_fc, mnist_conv, people_conv)', default = None)
args = parser.parse_args()

if args.mode == 'mnist_fc':
	from mnist_fc import Generator
elif args.mode == 'mnist_conv':
	from mnist_conv import Generator
elif args.mode == 'people_conv':
	from people_conv import Generator
else:
	exit()

G = Generator()
len_z = G.in_size

if args.input_file != None:
	serializers.load_hdf5(args.input_file, G)
else:
	print "You should select input file"
	exit()

batchsize = 25
z = Variable(np.random.uniform(-1,1,(batchsize,len_z)).astype(np.float32))
y1 = G(z,False)
fig = plt.figure()
ax = []
for i in xrange(batchsize):
	ax.append(fig.add_subplot(5,5,i+1))
	ax[i].imshow(np.array(y1.data[i]).reshape(G.imshape[1],G.imshape[2]),cmap='gray')
	ax[i].axis('off')

class callback(object):
	def suffle(self,event):
		z = Variable(np.random.uniform(-1,1,(batchsize,len_z)).astype(np.float32))
		y1 = G(z,False)
		for i in xrange(batchsize):
			ax[i].imshow(np.array(y1.data[i]).reshape(G.imshape[1],G.imshape[2]),cmap='gray')
		plt.draw()
c = callback()

axsuffle = plt.axes([0.8, 0.01, 0.1, 0.075])
button = Button(axsuffle, 'Suffle')
button.on_clicked(c.suffle)
plt.show()
