#!/usr/bin/python

# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

import time

import firebase_admin

from firebase_admin import credentials

from firebase_admin import db

import os

import glob

import serial

import subprocess

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

LED_OUT = 10

MOTION_IN = 8

device_file = ""

cred = credentials.Certificate('magicmirror-52b3f-firebase-adminsdk-oa09x-84946bee47.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://magicmirror-52b3f.firebaseio.com'
})

ref = db.reference('sensors/')

GPIO.setup(LED_OUT, GPIO.OUT)

GPIO.setup(MOTION_IN, GPIO.IN)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

print ("Sensor initializing............")

time.sleep(1);

print ('Sensor Ready....')

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def write_temp_to_serial():

    return read_temp() 

def alcohol_test():
    ser = serial.Serial("/dev/ttyACM0",9600, timeout=7)
    
    base_dir = '/dev/ttyACM0'
    line = ""

    line = ser.readline()
    #print(line)

    return line


def motion_detect():

	while True:

		if GPIO.input(MOTION_IN) == True:

			GPIO.output(LED_OUT, True)

			command = ('vcgencmd display_power 1')

			subprocess.call(command, shell=True)

		else:

			command = 'vcgencmd display_power 0'

			subprocess.call(command, shell=True)

			GPIO.output(LED_OUT, False)

	return 0

def writeToFirebase(alcohol_value, temperature_value):
    users_ref = ref.child('alcohol')
    users_ref.set({
    'value':  str(alcohol_value)
    })
    users_ref = ref.child('temperature')
    users_ref.set({
    'value' : str(temperature_value)
    })
    

while True:
    alc = alcohol_test()
    temp = read_temp()
    writeToFirebase(alc, temp )
