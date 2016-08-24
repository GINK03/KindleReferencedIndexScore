import chainer
import numpy as np
import chainer.functions as F
import chainer.links as L
from chainer import optimizers
from chainer import Variable
from chainer import serializers

import PIL.Image as Image
import matplotlib.pyplot as plt

def trainer(G,D,data,len_z=100,n_epoch=10000,pre_epoch=0,batchsize=500,save_interval=1000,
	output_dir=None,G_path=None,D_path=None,show=True):
	opt_g = optimizers.Adam(alpha=0.0002, beta1=0.5)
	opt_d = optimizers.Adam(alpha=0.0002, beta1=0.5)
	opt_g.setup(G)
	opt_d.setup(D)
	opt_g.add_hook(chainer.optimizer.WeightDecay(0.00001))
	opt_d.add_hook(chainer.optimizer.WeightDecay(0.00001))

	if D_path != None:
		serializers.load_hdf5("%s"%(D_path), D)
	if G_path != None:
		serializers.load_hdf5("%s"%(G_path), G)

	n_epoch += pre_epoch
	loss_d_mem =np.zeros(n_epoch-pre_epoch)
	loss_g_mem =np.zeros(n_epoch-pre_epoch)
	for epoch in xrange(pre_epoch,n_epoch):
		if epoch%10==0: print 'epoch',epoch
		perm = np.arange(len(data))
		np.random.shuffle(perm)
		for i in xrange(0,len(data),batchsize):
			z = Variable(np.random.uniform(-1,1,(batchsize, len_z)).astype(np.float32))
			y1 = G(z)
			y2 = D(y1)
			# discriminator
			loss_d = F.sigmoid_cross_entropy(y2,Variable(np.zeros((batchsize,1),dtype=np.int32)))
			loss_g = F.sigmoid_cross_entropy(y2,Variable(np.ones((batchsize,1),dtype=np.int32)))

			# get images
			images = data[perm[i:i+batchsize]]
			y2 = D(Variable(images))
			loss_d += F.sigmoid_cross_entropy(y2,Variable(np.ones((images.shape[0],1),dtype=np.int32)))

			loss_d_mem[epoch-n_epoch] += loss_d.data
			loss_g_mem[epoch-n_epoch] += loss_g.data

			opt_g.zero_grads()
			loss_g.backward()
			opt_g.update()

			opt_d.zero_grads()
			loss_d.backward()
			opt_d.update()
		#save model
		if (epoch+1)%save_interval == 0:
			z = Variable(np.random.uniform(-1,1,(10, len_z)).astype(np.float32))
			confirm = G(z,False)
			if output_dir != None:
				serializers.save_hdf5("%s/gan_model_dis%d.h5"%(output_dir,epoch+1), D)
				serializers.save_hdf5("%s/gan_model_gen%d.h5"%(output_dir,epoch+1), G)
				serializers.save_hdf5("%s/current_gen.h5"%(output_dir), G)
				if show:
					if D.imshape[0] == 3:
						plt.imshow(np.swapaxes(np.swapaxes(confirm.data[0], 0, 2),0,1))
					else:
						plt.imshow(confirm.data[0].reshape(D.imshape[1],D.imshape[2]),cmap="gray")
					plt.axis('off')
					plt.savefig('%s/image%d.jpg'%(output_dir,epoch+1))
			print '--%d--'%(epoch+1)
			print 'p_g    :',D(confirm,False).data[0]
			print 'p_delta:', D(Variable(images),False).data[0]
	print 'done'
	return loss_g_mem,loss_d_mem
