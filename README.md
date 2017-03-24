# Raspberry_pi_image_classifier
Takes an image on a raspberry pi camera and sends it via a server to a classifier

What each file does:
  - trainimgs.py: uses keras to read images and pass them through a convolutional neural net. The model and weights are then stored in 'model.json' and 'weights-Test-CNN.h5', respectively.
  - predictbasedonweights.py: using the files saved by 'trainimgs.py', this file takes in an image, formats it, and classifies it.
  - raspicomm.js: creates a server at port 3000. Upon a post request, the file saves the posted image and runs it through 'predictbasedonweights.py'. The output is then used as a response. 

Things you need to create in order for this to work:
  - InputData folder: stores training data
  - ResizedInputData folder: stores nothing at first; the classifier puts resized versions of the input data in that folder during runtime
  - Temp folder: stores the image sent over the server created in 'raspicomm.js'

