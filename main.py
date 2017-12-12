import numpy as np
from scipy import stats
from time import sleep
from picamera import PiCamera
import picamera.array
import cv2
import gpiozero

#initialize list containing servo objects and set them all to min position
servo_list = []
for k in range(8, 16):
	servo = gpiozero.Servo(k)
	servo_list.append(servo)
	servo.min()

#calculates the sensitivity for the algorithm which turn the images into
#song. is run once at the start of the main algorithm
#works by first placing a blank piece of paper in front of the camera
#a picture is then taken and the value of the darkest pixel of the paper is
#taken this value is then the thresehold value for deciding if a pixel value
#is filled in or not	
def calibrate(cam):
	with picamera.array.PiRGBArray(cam) as stream:
		cam.capture(stream, format='bgr')
		image = stream.array
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = image[90:430, 310:330]
	minval = int(np.min(image))
	return minval

#main algorithm - constantly takes picture, converts to length 8 array consisting
#of boolean 1s and 0s which determine which notes are played at that time step
with PiCamera() as cam:
	cam.start_preview()
	sleep(2)
	print('Camera Ready', end='\n\n')
	print('Place paper for calibration')
	thresehold = calibrate(cam)
	print('Calibration successfull. Feed art')
	
	while True:
		with picamera.array.PiRGBArray(cam) as stream:
                        #capture image
			cam.capture(stream, format='bgr')
			image = stream.array
			#convert image to greyscale
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			#crop image to focus on central column
			image = image[90:430, 310:330]
			#for each pixel sets the value to 1 if it is less than
			#thresehold and 0 is it is more than thresehold
			image = stats.threshold(image, threshmin=thresehold, newval=1)
			image = stats.threshold(image, threshmax=thresehold+1, newval=0)
			#scale the image down to a length 8 array consisting of
			#1s and 0s
			image = cv2.resize(image, (1, 8), interpolation=cv2.INTER_CUBIC)
			#ensures that valus are between 1 and 0
			image = np.clip(image, 0, 1)

                        #ensures that no 2 consecutive notes are played at once
			#for harmony
			for x in range(len(image)-1):
				if image[x][0]==1 and image[x+1][0]==1:
					image[x+1]=0
			#for each item in the array, if it is equal to 1, play
			#that note by actuating the servo
			for x in range(len(image)):
				if image[x][0]==1:
					servo_list[x].max()
			#delay before taking another picture and playing again
			sleep(1)
			#reset all servo positions
			for servo in servo_list:
				servo.min()
