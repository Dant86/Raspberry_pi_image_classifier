#Import Necessary Libraries
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,adam
from keras.utils import np_utils
from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import theano
from PIL import Image
from numpy import *
from sklearn.utils import shuffle
import sys
import warnings

def main():
	warnings.filterwarnings('ignore')

	#Image dimensions
	img_rows, img_cols = 200, 200

	#Load model from JSON
	json_file = open('model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)

	#Load weights into model
	loaded_model.load_weights('weights-Test-CNN.h5')

	#get image and reconfigure it to run through classifier
	img = Image.open('Temp/' + sys.argv[1])
	img = img.resize((img_rows,img_cols))
	img = img.convert('L')
	img.save('Temp/' + sys.argv[1], "JPEG")

	#turn image into array and predict
	immatrix = array([array(Image.open('Temp/' + sys.argv[1])).flatten()],'f')
	immatrix = immatrix.reshape(immatrix.shape[0], 1, img_rows, img_cols)
	immatrix = immatrix.astype('float32')
	immatrix /= 255
	a = loaded_model.predict(immatrix)

	#parse prediction
	max = 0
	index = 0
	for i in range(len(a[0])):
		if(a[0][i] > max):
			max = a[0][i]
			index = i
	if(index == 0):
		name = "eric"
	elif(index == 1):
		name = "luke"
	else:
		name = "mike"
	print(name + " with %d" % (max*100) + " percent certainty")
	sys.stdout.flush()

if __name__ == "__main__":
    main()






