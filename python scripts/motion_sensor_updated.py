#!/usr/bin/python

# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

import time

import os

import glob

import serial

import subprocess

from subprocess import Popen, PIPE, STDOUT

GPIO.setmode(GPIO.BOARD)

LED_OUT = 10

MOTION_IN = 8

device_file = ""

def initialize_all():

    #ser = serial.Serial('/dev/ttyACM0', 115200)

    GPIO.setup(LED_OUT, GPIO.OUT)

    GPIO.setup(MOTION_IN, GPIO.IN)

    os.system('modprobe w1-gpio')

    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'

    device_folder = glob.glob(base_dir + '28-01be4007010c')[0]

    device_file = device_folder + '/w1_slave'

    print ("Sensor initializing............")

    time.sleep(1);

    print ('Sensor Ready....')

    return 0

def motion_detect():

    while True:

        if GPIO.input(MOTION_IN) == True:

            print ('Motion Detected!!!!\n')

            GPIO.output(LED_OUT, True)

            command = ('vcgencmd display_power 1')

            subprocess.call(command, shell=True)

        else:

            command = 'vcgencmd display_power 0'

            subprocess.call(command, shell=True)

            print ('No one Here\n')

            GPIO.output(LED_OUT, False)

    return 0


def temperature_read():

    f = open(device_file, 'r')

    lines = f.readlines()

    print(lines)

    f.close()

    return lines

def read_temp():

    lines = temperature_read()

    while lines[0].strip()[-3:] != 'YES':

        time.sleep(0.2)

        lines = temperature_read()

        equals_pos = lines[1].find('t=')

    if equals_pos != -1:

        temp_string = lines[1][equals_pos+2:]

        temp_c = float(temp_string) / 1000.0

        temp_f = temp_c * 9.0 / 5.0 + 32.0

    return temp_c, temp_f


def write_temp_to_serial():

	print(read_temp())

    	return 0


#initializes all sensors and variables

initialize_all()

#reads to check if motion has been detected from the sensor

motion_detect()

#reads temperature values from the temp* sensor

temperature_read()

#writes the read temperature value to the serial port 
#which will be then read from NodeJs

write_temp_to_serial()
