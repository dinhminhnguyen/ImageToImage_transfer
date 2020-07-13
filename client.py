from __future__ import print_function
from torch import load
from numpy import vstack
from matplotlib import pyplot
import numpy as np
from PIL import Image
from keras.models import load_model
from keras_contrib.layers.normalization.instancenormalization import InstanceNormalization

def show_plot(imagesX, imagesY1, imagesY2):
	images = vstack((imagesX, imagesY1, imagesY2))
	titles = ['Real', 'Generated', 'Reconstructed']
	# scale from [-1,1] to [0,1]
	images = (images + 1) / 2.0
	# plot images row by row
	for i in range(len(images)):
		# define subplot
		pyplot.subplot(1, len(images), 1 + i)
		# turn off axis
		pyplot.axis('off')
		# plot raw pixel data
		pyplot.imshow(images[i])
		# title
		pyplot.title(titles[i])
	pyplot.show()

path = 'C:\\Users\\ASUS\\Documents\\Learning\\Machine Learning\\summer2winter_yosemite\\testA\\2010-09-07 12_23_20.jpg'
cust = {'InstanceNormalization': InstanceNormalization}
model_AtoB = load_model('C:\Users\ASUS\Desktop\projectPython\Image2Image_transfer\path\models\g_model_AtoB_007700.h5', cust)
model_BtoA = load_model('C:\Users\ASUS\Desktop\projectPython\Image2Image_transfer\path\models\g_model_BtoA_000500.h5', cust)

A_real = Image.open(path)
A_real = np.array(A_real)
A_real = (A_real - 127.5) / 127.5
A_real = (A_real + 1) / 2.0
A_real = A_real[np.newaxis, :]
B_generated = model_BtoA.predict(np.array(A_real))
A_reconstructed = model_AtoB.predict(B_generated)
print(B_generated.shape)
print(B_generated.shape)
show_plot(A_real, B_generated, A_reconstructed)
B_generated = B_generated[0 , :, :, :]
B_generated = Image.fromarray((B_generated*256).astype(np.uint8)).convert('RGB')
B_generated.save("static/uploads/copy.jpg")

