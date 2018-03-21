#/usr/bin/env python

def Normal(message):
   #Normal Flight
   return message


def Front(message):
   #Object to the front
   message[2] = bytearray.fromhex("64")
   message[3] = bytearray.fromhex("0b")
   return message


def Left(message):
   #Object to the left
   message[1] = bytearray.fromhex("94")
   message[2] = bytearray.fromhex("06")
   return message


def Rear(message):
   #Object to the rear
   message[2] = bytearray.fromhex("a4")
   message[3] = bytearray.fromhex("34")
   return message


def Right(message):
   #Object to the right
   message[2] = bytearray.fromhex("bc")
   message[3] = bytearray.fromhex("01")
   return message


directionFlags = {0:Normal,
			1:Front,
			2:Left,
			4:Rear,
			8:Right,
}
      
if __name__ == "__main__":
   import serial
   import time
   import pigpio
   import srte
   
   #SBUS Definition (1 startbit, 8 databits, 1 odd parity, 2 stopbits)
   port = serial.Serial('/dev/ttyAMA0')
   port.baudrate = 100000
   port.bytesize = 8
   port.parity = serial.PARITY_ODD
   port.stopbits = 2
   port.timeout = 3

   pi = pigpio.pi() 

   if not pi.connected:
       exit()

   S=[] #this will hold sensor objects
   Readings = [0,0,0,0,0,0,0,0] #the most recent reading values from the sensor
   S.append(srte.sonar(pi, 03, 04))
   S.append(srte.sonar(pi, 14, 15))
   S.append(srte.sonar(pi, 17, 27)) #sensor trigger pin 17/ echo pin 27
   S.append(srte.sonar(pi, 23, 24)) #sensor trigger pin 23/ echo pin 24
   end = time.time() + 30.0
  
   r = 1
   port.write(bytearray.fromhex("0f 00 04 20 00 01 38 3f 00 fe 27 00 01 08 40 00 02 10 80 00 04 20 00 00 00")
   try:
        while time.time() < end:
            #get sbus message
            message = port.read(25)
            
            #directional flag to determine which direction to avoid 
	    #bits are defined as right,rear,left,front where a 1 in that bit
	    # means an object is present that direction
            direction = 0

            for s in S: #iterate through each sensor
                s.trigger()

            time.sleep(0.01)

            for s in range(len(S)):#read each sensor and store in readings array
                Readings[s] = S[s].read()
                if (Readings[s] <= 100):
                    if (s == 0 or s == 1):#front sensors
                        direction = direction | 1
                    if (s == 2 or s == 3):#left sensors
                        direction = direction | 2
                    if (s == 4 or s == 5):#rear sensors
                        direction = direction | 4
                    if (s == 6 or s == 7):#right sensors
                        direction = direction | 8
                #print("{} {:.1f}".format(r, Readings[s]))
            message = directionFlags[direction](message)
            print (' ' .join(x.encode('hex') for x in message))
            port.write(message)

            r += 1


   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   for s in S:
      s.cancel()
   print Readings #print recent readings
   print r
   pi.stop()
