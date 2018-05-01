#/usr/bin/env python
import numpy as np
from scipy import signal
#import matplotlib.pyplot as plt
import serial
import time
import RPi.GPIO as GPIO
import binascii

def Normal(message):
   #Normal Flight
   return str(message)


#Avoid object to the front
def Front(message):
   #print ("front")
   temp = list(str(message))
   temp[2] = binascii.unhexlify('64')
   temp[3] = binascii.unhexlify('0b')
   return "".join(temp)


#Avoid object to the left
def Left(message):
   #print ("left")
   temp = list(str(message))
   temp[1] = binascii.unhexlify('94')
   temp[2] = binascii.unhexlify('06')
   return "".join(temp)

#Avoid object to the rear
def Rear(message):
   #print ("Rear")
   temp = list(str(message))
   temp[2] = binascii.unhexlify('a4')
   temp[3] = binascii.unhexlify('34')
   return "".join(temp)

#Avoid object to the right
def Right(message):
   #print ("Right")
   temp = list(message)
   temp[1] = binascii.unhexlify('bc')
   temp[2] = binascii.unhexlify('01')
   return "".join(temp)

def Panic(message):
   message =  binascii.unhexlify("0f000420000138bf0217380001084000021080000420000000")
   return message
#which direction to avoid
directionFlags = {0:Normal,
			1:Front, #object front
			2:Left,  #object left
            		3:Front, #object front and left
			4:Rear,  #object rear
   	                5:Right, #object front and rear
		        6:Rear,  #object rear and left
		        7:Left,  #object front, rear, and left
			8:Right, #Object right
	                9:Front, #object front and right
	                10:Rear, #object right and left
	                11:Front, #object right left and front
	                12:Rear, #object right and rear
           	  	13:Right, #object front and rear and right
     		        14:Rear, #object rear, left, right
           		15:Panic, #object everywhere
}


def trigger(TRIG):
   GPIO.output(TRIG,True)
   time.sleep(.000015)
   GPIO.output(TRIG,False)

def kalman(z):

    # intial parameters
    n_iter = len(z)
    sz = (n_iter,) # size of array
    #x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
    # z is observations (normal about x, sigma=0.1)

    Q = 1e-5 # process variance

    #allocate space for arrays
    xhat=np.zeros(sz)     # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)   # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor
    R = 20**2 #estimate of measurement variance, change to see effect

    #intial guesses
    xhat[0] = 0.0
    P[0] = 35.0

    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q

       # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
    #time.sleep(1)
    return xhat[r[s]]	
	
if __name__ == "__main__":
   GPIO.setmode(GPIO.BCM)

   #SBUS Definition (1 startbit, 8 databits, 1 odd parity, 2 stopbits)
   port = serial.Serial('/dev/ttyAMA0')
   port.baudrate = 100000
   port.bytesize = 8
   port.parity = serial.PARITY_ODD
   port.stopbits = 2
   port.timeout = 6

   #front
   GPIO.setup(4,GPIO.OUT)
   GPIO.setup(17,GPIO.IN)
   #left
   GPIO.setup(27,GPIO.OUT)
   GPIO.setup(22,GPIO.IN)
   #rear
   GPIO.setup(05,GPIO.OUT)
   GPIO.setup(06,GPIO.IN)
   #right
   GPIO.setup(13,GPIO.OUT)
   GPIO.setup(19,GPIO.IN)
   #front/left
   GPIO.setup(26,GPIO.OUT)
   GPIO.setup(21,GPIO.IN)
   #front/right
   GPIO.setup(16,GPIO.OUT)
   GPIO.setup(20,GPIO.IN)
   #rear/right
   GPIO.setup(25,GPIO.OUT)
   GPIO.setup(12,GPIO.IN)
   #rear/left
   GPIO.setup(23,GPIO.OUT)
   GPIO.setup(24,GPIO.IN)

   S=[[4,17],[27,22],[05,06],[13,19],[26,21],[16,20],[25,12],[23,24]] #this will hold sensor GPIO channel numbers {trig/echo,}
   Readings = np.ones((8,15)) #the most recent reading values from the sensor
   LIMIT = 5 #minimum distance
   r = np.zeros(8) #last updated location

   def Update(s,value):
	
	x = (Readings[s])
	x = np.append(x,value)
	xhat = signal.savgol_filter(x,11,3)
	test = np.delete(Readings[s],0)
	Readings[s] = np.append(test, xhat[14])
	
   count = 1
   direction = 0
   #try to correct wrong order
   first = binascii.unhexlify("0f000420000138bf0217380001084000021080000420000000")
   startcommand = binascii.unhexlify("0f6c610b5b283dbf0217380001084000021080000420000000")
   while (port.read(25) != first):
      test = port.read(1)

   try:
        while 1:
            for s in range(len(S)): #iterate through each sensor
		#time.sleep(.09)
                if (direction == 0):
                   message = port.read(25)
                   port.write(message)

                trigger(S[s][0])

        	while (GPIO.input(S[s][1]) == 0):
                    start_time = time.time()
        	while (GPIO.input(S[s][1]) == 1):
                    stop_time = time.time()
                    if (stop_time - start_time >= .018): #timeout after 18ms
                        break

		
                Update(s,((stop_time-start_time)*34029/2)) #update reading in cm
                if (Readings[s][r[s]] <= LIMIT):
                    if (s == 0):#front sensors
                        direction = direction | 1 #0001
                    elif (s == 1):#left sensors
                        direction = direction | 2 #0010
                    elif (s == 2):#rear sensors
                        direction = direction | 4 #0100
                    elif (s == 3):#right sensors
                        direction = direction | 8 #1000
                    elif (s == 4):#topleft sensors
                        direction = direction | 3 #0011
                    elif (s == 5):#topright sensors
                        direction = direction | 9 #1001
                    elif (s == 6):#bottomright sensors
                        direction = direction | 12 #1100
                    elif (s == 7):#bottemleft sensors
                        direction = direction | 6 #0110


                else:
                    if (s == 0 and Readings[0][r[0]] >= LIMIT and Readings[4][r[4]] >= LIMIT and Readings[5][r[5]] >= LIMIT):#front sensors
                        direction = direction & 14 #1110
                    elif ( s == 1 and Readings[1][r[1]] >= LIMIT and Readings[4][r[4]] >= LIMIT and Readings[7][r[7]] >= LIMIT):#left sensors
                        direction = direction & 13
                    elif ( s == 2 and Readings[2][r[2]] >= LIMIT and Readings[6][r[6]] >= LIMIT and Readings[7][r[7]] >= LIMIT):#rear sensors
                        direction = direction & 11
                    elif ( s == 3 and Readings[3][r[3]] >= LIMIT and Readings[6][r[6]] >= LIMIT and Readings[5][r[5]] >= LIMIT):#right sensors
                        direction = direction & 7

                print("{} {:.1f}".format(count, Readings[s][r[s]]))
                while (time.time() - start_time <= .045):
		    message = port.read(25)
                    message = directionFlags[direction](message)
                    #message = directionFlags.setdefault(direction,message)(message)
            	    #print (' ' .join(x.encode('hex') for x in message))
                    port.write(message)

            count += 1
            time.sleep(.001)

   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   print Readings #print recent readings
   print count
   GPIO.cleanup()
