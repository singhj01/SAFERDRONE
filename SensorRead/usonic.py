#/usr/bin/env python
def Normal():
    test = 1;
   # print ("Normal Flight")
def Front():
    test = 1;
   # print ("Object to the front")
def Left():
    test = 1;
   # print ("Object to the left")
def Rear():
    test = 1;
   # print ("Object to the rear")
def Right():
    test = 1;
   # print ("object to the right")

directionFlags = {0:Normal,
			1:Front,
			2:Left,
			4:Rear,
			8:Right,
}
      
if __name__ == "__main__":

   import time
   import pigpio
   import srte

   pi = pigpio.pi()

   if not pi.connected:
       exit()

   S=[] #this will hold sensor objects
   Readings = [0,0,0,0,0,0,0,0] #the most recent reading values from the sensor
   S.append(srte.sonar(pi, 17, 27)) #sensor trigger pin 17/ echo pin 27
   S.append(srte.sonar(pi, 23, 24)) #sensor trigger pin 23/ echo pin 24
   end = time.time() + 30.0
  


   r = 1

   try:
        while time.time() < end:
            #directional flags to determine which direction to avoid 
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
                #print r
            directionFlags[direction]()
            time.sleep(0.005)

            r += 1


   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   for s in S:
      s.cancel()
   print Readings #print readings
   print r
   pi.stop()
