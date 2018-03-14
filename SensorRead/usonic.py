#/usr/bin/env python
def avoid(flagFront,flagRear,flagLeft,flagRight,):
    if (!flagFront && !flagRear && !flagRight && !flagLeft):
        print("Normal Flight")
    else if (flagFront && !flagRear && !flagRight && !flagLeft):
        print("Object in front")
    else if (!flagFront && flagRear && !flagRight && !flagLeft):
        print("Object in rear")
    else if (!flagFront && !flagRear && flagRight && !flagLeft):
        print("Object on right")
    else if (!flagFront && !flagRear && !flagRight && flagLeft):
        print("Object on Left")
    else:
        print("Your surrounded")

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
   end = time.time() + 1.0
   flagFront = False
   flagLeft = False
   flagRight = False
   flagRear = False

   r = 1

   try:
      while time.time() < end:

        for s in S: #iterate through each sensor
            s.trigger()

        time.sleep(0.02)

        for s in range(len(S)):#read each sensor and store in readings array
            Readings[s] = S[s].read()
            if (readings[s] <= 50):
                if (s == 0 or s == 1):
                    flagFront = True
                if (s == 2 or s == 3):
                    flagRight = True
                if (s == 4 or s == 5):
                    flagRear = True
                if (s == 6 or s == 7):
                    flagFront = True
	    print("{} {:.1f}".format(r, Readings[s]))

        time.sleep(0.01)
        avoid(flagFront,flagRear,flagLeft,flagRight)


        r += 1


   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   for s in S:
      s.cancel()
   print (Readings) #print readings
   pi.stop()
