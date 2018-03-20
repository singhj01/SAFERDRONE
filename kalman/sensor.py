#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


TRIG1=23
ECHO1=24
TRIG2=17
ECHO2=27

try:
        while(True):

                #test = input()
                GPIO.setmode(GPIO.BCM)
                print "Left Sensor"

                GPIO.setup(TRIG1,GPIO.OUT)
                GPIO.setup(ECHO1,GPIO.IN)

                GPIO.output(TRIG1,False)
                print " waiting for stuff"
                time.sleep(.0069)

                GPIO.output(TRIG1,True)
                time.sleep(0.00001)
                GPIO.output(TRIG1,False)


                while GPIO.input(ECHO1)==0:

                  pulse_start = time.time()

                while GPIO.input(ECHO1)==1:

                  pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance*.3937, 2)

                print "Distance:",distance,"in"
                #print "Error:",test-distance, "in"
                # GPIO.cleanup()
