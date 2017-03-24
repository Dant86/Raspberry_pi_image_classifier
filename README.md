# Raspberry_pi_image_classifier
Takes an image on a raspberry pi camera and sends it via a server to a classifier

Things you need to create in order for this to work:
  - InputData folder: stores training data
  - ResizedInputData folder: stores nothing at first; the classifier puts resized versions of the input data in that folder during runtime
  - Temp folder: stores the image sent over the server created in 'raspicomm.js'
