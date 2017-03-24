#Import Libraries
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,adam
from keras.utils import np_utils
from keras.models import model_from_json
import numpy as np
import os
import theano
from PIL import Image
from numpy import *
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

# input image dimensions
img_rows, img_cols = 200, 200

# number of channels
img_channels = 1

path1 = 'InputData'    #path of folder of images    
path2 = 'ResizedInputData'  #path of folder to save images    

listing = os.listdir(path1) 
num_samples=size(listing)
print(num_samples)

#Resize images and convert to grayscale
for file in listing:
    im = Image.open(path1 + '/' + file)   
    img = im.resize((img_rows,img_cols))
    gray = img.convert('L')       
    gray.save(path2 +'/' +  file, "JPEG")

imlist = os.listdir(path2)

im1 = array(Image.open('ResizedInputData' + '/'+ imlist[0])) # open one image to get size
m,n = im1.shape[0:2] # get the size of the images
imnbr = len(imlist) # get the number of images

# create matrix to store all flattened images
immatrix = array([array(Image.open('ResizedInputData'+ '/' + im2)).flatten()
              for im2 in imlist],'f')           

label=np.ones((num_samples,),dtype = int)
label[0:10]=0
label[10:20]=1
label[20:]=2

#Shuffle data so classifier doesn't recognize index patterns
data,Label = shuffle(immatrix,label, random_state=2)
train_data = [data,Label]

#batch_size to train
batch_size = 32
# number of output classes
nb_classes = 3
# number of epochs to train
nb_epoch = 20
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
nb_conv = 3

(X, y) = (train_data[0],train_data[1])

#Split X and y into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

#Initialize model
model = Sequential()

model.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                        border_mode='valid',
                        input_shape=(1, img_rows, img_cols)))
convout1 = Activation('relu')
model.add(convout1)
model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
convout2 = Activation('relu')
model.add(convout2)
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

#Train now
print(np.shape(X_train))
hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
              verbose=1, validation_data=(X_test,Y_test))
            
            
hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
              verbose=1)


score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score)
print(model.predict_classes(X_test[1:5]))
print(Y_test[1:5])

#Confusion matrix
from sklearn.metrics import classification_report,confusion_matrix

Y_pred = model.predict(X_test)
print(Y_pred)
y_pred = np.argmax(Y_pred, axis=1)
print(y_pred)

p=model.predict_proba(X_test) # to predict probability

#Save weights
fname = "weights-Test-CNN.h5"
model.save_weights(fname,overwrite=True)
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

#Save model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()