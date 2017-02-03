import os

import numpy
from PIL import Image, ImageDraw, ImageFont
import six

import numpy as np

from io import BytesIO
import os
import pickle
import json
import numpy as np

import skimage.io as io

from chainer.dataset import dataset_mixin

class GenFontsImage():
  def __init__(self):
    self.OUTDIR = 'fonts.aoyagi'
    import glob
    self.source = set(''.join([open(f).read().replace('\n', '') for f in glob.glob('./text_source/*')]))
    pass
  
  def generate(self):
    for word in self.source:
      t = np.zeros((300, 300, 3)).astype('uint8')
      t += 255
      to_save_img = Image.fromarray(t)
      draw = ImageDraw.Draw(to_save_img)
      font = ImageFont.truetype("/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf", 200)
      draw.text((50,50), word, (0, 0, 0),font=font)
      to_save_img.save('./%s/%s.org.jpg'%(self.OUTDIR, word) ) 
    
    for word in self.source:
      t = np.zeros((300, 300, 3)).astype('uint8')
      t += 255
      to_save_img = Image.fromarray(t)
      draw = ImageDraw.Draw(to_save_img)
      #font = ImageFont.truetype("./PixelMplus12-Regular.ttf", 200)
      font = ImageFont.truetype("./aoyagireisyosimo_ttf_2_01.ttf", 200)
      draw.text((50,50), word, (0, 0, 0),font=font)
      to_save_img.save('./%s/%s.cnv.jpg'%(self.OUTDIR, word) ) 

if __name__ == '__main__':
    #vec = VecDataset( None )
    gen_fonts_image = GenFontsImage()
    gen_fonts_image.generate()
