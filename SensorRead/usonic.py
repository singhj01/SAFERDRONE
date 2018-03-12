#/usr/bin/env python
if __name__ == "__main__":

   import time
   import pigpio
   import srte

   pi = pigpio.pi()

   if not pi.connected:
      exit()

   S=[]
   Readings = [0,0,0,0,0,0,0,0]
   S.append(srte.sonar(pi, 17, 27))
   S.append(srte.sonar(pi, 23, 24))
   end = time.time() + 1.0

   r = 1

   try:
      while time.time() < end:

         for s in S:
            s.trigger()

         time.sleep(0.02)

         for s in range(len(S)):
            Readings[s] = S[s].read()
	    print("{} {:.1f}".format(r, Readings[s]))

         time.sleep(0.02)

         r += 1

   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   for s in S:
      s.cancel()
   print (Readings)
   pi.stop()
