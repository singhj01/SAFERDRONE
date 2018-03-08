#/usr/bin/env python
if __name__ == "__main__":

   import time
   import pigpio
   import srte

   pi = pigpio.pi()

   if not pi.connected:
      exit()

   S=[]
   S.append(srte.sonar(pi, 17, 27))

   end = time.time() + 30.0

   r = 1

   try:
      while time.time() < end:

         for s in S:
            s.trigger()

         time.sleep(0.03)

         for s in S:
            print("{} {:.1f}".format(r, s.read()))

         time.sleep(0.2)

         r += 1

   except KeyboardInterrupt:
      pass

   print("\ntidying up")

   for s in S:
      s.cancel()

   pi.stop()
