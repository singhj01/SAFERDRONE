#/usr/bin/env python

def Normal(message):
   #Normal Flight
   return str(message)


#Avoid object to the front
def Front(message):
   print ("front")
   temp = list(str(message))
   temp[2] = binascii.unhexlify('64')
   temp[3] = binascii.unhexlify('0b')
   return "".join(temp)


#Avoid object to the left
def Left(message):
   print ("left")
   temp = list(str(message))
   temp[1] = binascii.unhexlify('94')
   temp[2] = binascii.unhexlify('06')
   return "".join(temp)

#Avoid object to the rear
def Rear(message):
   print ("Rear")
   temp = list(str(message))
   temp[2] = binascii.unhexlify('a4')
   temp[3] = binascii.unhexlify('34')
   return "".join(temp)

#Avoid object to the right
def Right(message):
   print ("Right")
   temp = list(message)
   temp[2] = binascii.unhexlify('bc')
   temp[3] = binascii.unhexlify('01')
   return "".join(temp)


directionFlags = {0:Normal,
			1:Front,
			2:Left,
			4:Rear,
			8:Right,
}


def trigger(TRIG):
   GPIO.output(TRIG,True)
   time.sleep(.00001)
   GPIO.output(TRIG,False)


if __name__ == "__main__":
   import serial
   import time
   import RPi.GPIO as GPIO
   import binascii

   GPIO.setmode(GPIO.BCM)

   #SBUS Definition (1 startbit, 8 databits, 1 odd parity, 2 stopbits)
   port = serial.Serial('/dev/ttyAMA0')
   port.baudrate = 100000
   port.bytesize = 8
   port.parity = serial.PARITY_ODD
   port.stopbits = 2
   port.timeout = 6

   GPIO.cleanup()

   GPIO.setup(16,GPIO.OUT)
   GPIO.setup(20,GPIO.IN)

   GPIO.setup(13,GPIO.OUT)
   GPIO.setup(19,GPIO.IN)

   GPIO.setup(23,GPIO.OUT)
   GPIO.setup(24,GPIO.IN)

   GPIO.setup(17,GPIO.OUT)
   GPIO.setup(27,GPIO.IN)
   
   #S = [[0 for x in range(2)] for y in range(4)]
   S=[[16,20],[13,19],[23,24],[17,27]] #this will hold sensor GPIO channel numbers {trig/echo}
   Readings = [0,0,0,0,0,0,0,0] #the most recent reading values from the sensor
   posi = ['Top left','Top Right', 'Bottom Left', 'Bottom Right']
   #start_time = [0,0,0,0,0,0,0,0]
   #stop_time = [0,0,0,0,0,0,0,0]
   end = time.time() + 90.0

   r = 1
   direction = 0

   #potential interrupt code?
   #GPIO.add_event_detect(6,GPIO.FALLING,callback=mycallback)
   #def mycallback(channel):
   #   time = time.time()
   #   if (channel == 6):#front sensors
   #      direction = direction | 1
   #      stop_time[0] = time
   #      Readings[0] = (stop_time[0]-start_time[0])*34029/2
   #   if (channel == 19):#left sensors
   #      direction = direction | 2
   #      stop_time[1] = time
   #      Readings[1] = (stop_time[1]-start_time[1])*34029/2
   #   if (channel == 27):#rear sensors
   #      direction = direction | 4
   #      stop_time[2] = time
   #      Readings[2] = (stop_time[2]-start_time[2])*34029/2
   #   if (channel == 24):#right sensors
   #      direction = direction | 8
   #      stop_time[3] = time
   #      Readings[3] = (stop_time[3]-start_time[3])*34029/2



   #test code
   #first = bytearray.fromhex("0f 00 04 20 00 01 38 3f 00 fe 27 00 01 08 40 00 02 10 80 00 04 20 00 00 00")
   try:
        while time.time() < end:
            for s in range(len(S)): #iterate through each sensor
                if (direction == 0):
                   message = port.read(25)
                   port.write(message)
                trigger(S[s][0])
            #for s in range(len(S)):#read each sensor and store in readings array
		while (GPIO.input(S[s][1]) == 0):
                #GPIO.wait_for_edge(S[s][1],GPIO.RISING)
                   start_time = time.time()
		while (GPIO.input(S[s][1]) == 1):                
		#GPIO.wait_for_edge(S[s][1],GPIO.FALLING) #max echo at 20ms, this gives a max range of 340cm
                   stop_time = time.time()
                #except TimeoutError: #if timeout then continue and assume max distance
                #    stop_time = time.time()
		#    print ("Entered exception")

                Readings[s] = (stop_time-start_time)*34029/2
                if (Readings[s] <= 20):
                    if (s == 0):#front sensors
                        direction = direction | 1 #0001
                    elif (s == 1):#left sensors
                        direction = direction | 2 #0010
                    elif (s == 2):#rear sensors
                        direction = direction | 4 
                    elif (s == 3):#right sensors
                        direction = direction | 8
                else:
                    if (s == 0):#front sensors
                        direction = direction & 14 #1110
                    elif (s == 1):#left sensors
                        direction = direction & 13
                    elif (s == 2):#rear sensors
                        direction = direction & 11
                    elif (s == 3):#right sensors
                        direction = direction & 7

                print(posi[s] + "{} {:.1f}".format(r, Readings[s]))
            	message = directionFlags[direction](message)
                message = port.read(25)
                #message = directionFlags.setdefault(direction,message)(message)
            	#print (' ' .join(x.encode('hex') for x in message))
            	port.write(message)

            r += 1
            time.sleep(.005)

   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   print Readings #print recent readings
   print r
   GPIO.cleanup()
