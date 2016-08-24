import chainer
import numpy as np
import chainer.functions as F
import chainer.links as L
from chainer import optimizers
from chainer import Variable
from chainer import serializers

import matplotlib.pyplot as plt
import PIL.Image as Image
import argparse
from trainer import trainer
import sys
sys.path.append('./networks')

parser = argparse.ArgumentParser()
parser.add_argument('--output_dir','-o',default = None)
parser.add_argument('--dis','-d',default = None)
parser.add_argument('--gen','-g',default = None)
parser.add_argument('--pre_epoch','-e',type=int,default = 0)
parser.add_argument('--n_epoch','-n',type=int,default = 10000)
parser.add_argument('--save_interval','-s',type=int,default = 5000)
parser.add_argument('--batchsize','-b',type=int,default = 401)
parser.add_argument('--mode','-m',help = 'Train mode (mnist_fc, mnist_conv, people)', default = None)
parser.add_argument('--dataset','-ds',help = 'Dataset (mnist, people)', default = None)

args = parser.parse_args()

if args.mode == None: exit()

print 'fetch data...'

if args.dataset == 'mnist':
	from sklearn.datasets import fetch_mldata
	data = fetch_mldata('MNIST original', data_home=".")
	images = np.array(data.data).astype(np.float32)
	images = images.reshape(images.shape[0],28,28)
elif args.dataset == 'people':
	from sklearn.datasets import fetch_lfw_people
	data = fetch_lfw_people()
	images = np.array(data.images).astype(np.float32)
else:
	print 'Select dataset from (mnist, people)'
	exit()

if args.mode == 'mnist_fc':
	from mnist_fc import Generator, Discriminator
elif args.mode == 'mnist_conv':
	from mnist_conv import Generator, Discriminator
elif args.mode == 'people':
	from people_conv import Generator, Discriminator
else:
	print 'Select mode from (mnist_fc, mnist_conv, people)'
	exit()

print 'done fetch data'

images /= 255


G = Generator()
D = Discriminator()
z_shape = G.in_size
imshape = D.imshape

data = np.zeros((images.shape[0],imshape[0],imshape[1],imshape[2])).astype(np.float32)
for i in xrange(images.shape[0]):
	data[i,:] = np.asarray(Image.fromarray(images[i]).resize((imshape[1],imshape[2])))

print 'start training'
loss_g_mem,loss_d_mem = trainer(G,D,data,len_z=z_shape,batchsize=args.batchsize,save_interval=args.save_interval,output_dir=args.output_dir,n_epoch=args.n_epoch,pre_epoch=args.pre_epoch,G_path=args.gen,D_path=args.dis)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(args.n_epoch-args.pre_epoch),loss_d_mem,'r')
ax.plot(range(args.n_epoch-args.pre_epoch),loss_g_mem,'b')
plt.title('loss')
plt.show()

plt.show()