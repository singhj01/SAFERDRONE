
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
   #from pykalman import KalmanFilter
   pi = pigpio.pi()

   if not pi.connected:
       exit()

   S=[] #this will hold sensor objects
   Readings = [0,0,0,0,0,0,0,0] #the most recent reading values from the sensor
  # S.append(srte.sonar(pi, 17, 27)) #sensor trigger pin 17/ echo pin 27
   S.append(srte.sonar(pi, 13, 19)) #sensor trigger pin 23/ echo pin 24
   end = time.time() + 400.0



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
                Readings[s] = S[s].read()		#prior error covariance
		#while False:
		
		while r > 0:
			r = r - 1		#time update
			r += 1
		while Readings[s] >= 0:
			print Readings[s]	#measurement update
			Readings[s] +=  1
		#kalman gain
		k = r / (r + 113)		#113 = SNR with standard deviation = 0.05
	 	Readings[s] = Readings[s] + (k * (0.3 - Readings[s])) #updating the estimate
		r = (1- k) * r	#update error covariance
		
#		count = 100
#		newValue = Readings[s]
#		mean = newValue/count
#		def update(existingAggregate, newValue):
#			(count, mean, M2) = existingAggregate
#		        count = count + 1 
#		        delta = newValue - mean
#		        mean = mean + delta / count
#		        delta2 = newValue - mean
#		        M2 = M2 + delta * delta2

#		        return (count, mean, M2)

# retrieve the mean and variance from an aggregate
#		def finalize(existingAggregate):
#			(count, mean, M2) = existingAggregate
#		        (mean, variance) = (mean, M2/(count - 1)) 
#		        if count < 2:
#		        	return float('nan')
#		        else:
#			        return (mean, variance)		
		
#import random
#n_iter = Readings[s]
#actual_values = int([-0.37727 + j * j * 0.00001 for j in xrange (n_iter)])
#noisy_measurement = [random.random() * 2.0 - 1.0 + actual_val for actual_val in actual_values]
#import numpy
#measurement_standard_deviation = numpy.std([random.random() * 2.0 - 1.0 for j in xrange(n_iter)])
#process_variance = 1e-3
#estimated_measurement_variance = measurement_standard_deviation ** 2
#kalman_filter = KalmanFilter(process_variance, estimated_measurement_variance)
#posteri_estimate_graph = []		

#for iterations in xrange(1, n_iter):
#	kalman_filter.input_latest_noisy_measurement(noisy_measurement[iteration])
#	posteri_estimate_graph.append(kalman_filter.get_latest_estimated_measurement())




	#kf = KalmanFilter(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]])
        #measure = S[s].read()   
        #measure = np.Readings[s]
	#kf = kf.em(measure, n_iter = 5)			
	#(filtered_state_means, filtered_state_covariances) = kf.filter(measurements)
		if (Readings[s] <= 100):
                    if (s == 0 or s == 1):#front sensors
                        direction = direction | 1
                    if (s == 2 or s == 3):#left sensors
                        direction = direction | 2
                    if (s == 4 or s == 5):#rear sensors
                        direction = direction | 4
                    if (s == 6 or s == 7):#right sensors
                        direction = direction | 8
                print("{} {:.1f}".format(r, Readings[s])) # Readings[s]))
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
  #print r
   pi.stop()
