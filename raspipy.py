from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import requests

url = #put the url in here

#setup picamera
camera = PiCamera()

#setup GPIO at port 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	input_state = GPIO.input(18)
	if input_state == False:
		camera.capture('/home/pi/Desktop/img.jpeg')
		files = {'media': open('/home/pi/Desktop/img.jpeg','rb')
		requests.post(url,files=files)


