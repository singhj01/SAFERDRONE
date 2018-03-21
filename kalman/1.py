# -*- coding: utf-8 -*-
#!/usr/bin/env python
#Libraries
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.pylab as pylab

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
	    xs = range(100)
	    ys = []
	    x = -0.37727 #truth value
	    z = np.random.normal(x, 0.1, size = ys)
	   
	    Q = 1e-5
	    #allocate space for arrays
	    xhat=np.zeros(ys)     # a posteri estimate of x
	    P=np.zeros(ys)         # a posteri error estimate
	    xhatminus=np.zeros(ys) # a priori estimate of x
    	    Pminus=np.zeros(ys)   # a priori error estimate
	    K=np.zeros(ys)         # gain or blending factor
	    R = 0.1**2 #estimate of measurement variance, change to see effect

#intial guesses
	    xhat = [0.0]
	    P = [0.1]

	    for i in xs:
		ys.append(dist)
	   # plt.plot(xs, ys, label = ´Sample´)
	   # plt.show()


   # measurement update
	        K = Pminus/( Pminus+R )

                what = xhatminus+K*(z-xhatminus)
		#dist = what + dist
		P = (1-K)*Pminus
		dist = dist + P + K + what
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

