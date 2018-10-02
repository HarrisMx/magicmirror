import RPi.GPIO as GPIO
import time
import pyserial
import subprocess
from subprocess import Popen, PIPE, STDOUT

GPIO.setmode(GPIO.BOARD)
LED_OUT = 10
MOTION_IN = 8

def motion_start():

	GPIO.setup(LED_OUT,GPIO.OUT)
	GPIO.setup(MOTION_IN,GPIO.IN)

	print("Sensor initializing............")

	time.sleep(2)

	print("Sensor Ready....")
	return 0

def motion_detect():

	while True:
		if GPIO.input(MOTION_IN) == True :
			print("Motion Detected!!!!\n")
			GPIO.output(LED_OUT,True)
			command = "vcgencmd display_power 1"
			subprocess.call(command, shell=True)
		else:
			command = "vcgencmd display_power 0"
			subprocess.call(command, shell=True)
			print("No one Here\n")
			GPIO.output(LED_OUT,False)
	return 0


motion_start()
motion_detect()

