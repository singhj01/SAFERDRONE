#/usr/bin/env python

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
   Readings = [0,0,0,0,0,0,0,0] #the most recent reading values from the sensor
   LIMIT = 5 #minimum distance

   r = 1
   direction = 0
   #try to correct wrong order
   first = binascii.unhexlify("0f000420000138bf0217380001084000021080000420000000")
   startcommand = binascii.unhexlify("0f6c610b5b283dbf0217380001084000021080000420000000")
   while (port.read(25) != first):
      test = port.read(1)
      #print (' ' .join(x.encode('hex') for x in test))
   #while (port.read(25) != startcommand):
   #   print("waiting")
   
	
         
   try:
        while 1:
            for s in range(len(S)): #iterate through each sensor
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
                   

                Readings[s] = (stop_time-start_time)*34029/2 #reading in cm
                if (Readings[s] <= LIMIT):
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
                    if (s == 0 and Readings[0] >= LIMIT and Readings[4] >= LIMIT and Readings[5] >= LIMIT):#front sensors
                        direction = direction & 14 #1110
                    elif ( s == 1 and Readings[1] >= LIMIT and Readings[4] >= LIMIT and Readings[7] >= LIMIT):#left sensors
                        direction = direction & 13
                    elif ( s == 2 and Readings[2] >= LIMIT and Readings[6] >= LIMIT and Readings[7] >= LIMIT):#rear sensors
                        direction = direction & 11
                    elif ( s == 3 and Readings[3] >= LIMIT and Readings[6] >= LIMIT and Readings[6] >= LIMIT):#right sensors
                        direction = direction & 7

                print("{} {:.1f}".format(r, Readings[s]))
                while (time.time() - start_time <= .045):                  
		   message = port.read(25)
                   message = directionFlags[direction](message)
                   #message = directionFlags.setdefault(direction,message)(message)
            	   print (' ' .join(x.encode('hex') for x in message))
                   port.write(message)

            r += 1
            time.sleep(.005)

   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   print Readings #print recent readings
   print r
   GPIO.cleanup()
