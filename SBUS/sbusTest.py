#!/usr/bin/env python 
import serial
import time
#Define UART Port
#1 startbit, 8 databits, 1 odd parity, 2 stopbits
port = serial.Serial('/dev/ttyAMA0')
port.baudrate = 100000
port.bytesize = 8
port.parity = serial.PARITY_ODD
port.stopbits = 2
port.timeout = 6

#loops to display 20 messages 
#for x in range(10):
while(1):
    #read 9 bytes of data per message
    rcv = port.read(25)
    #display in HEX format
    print (' ' .join(x.encode('hex') for x in rcv))
    port.write(rcv)
    #print (rcv)
    #print (' '.join(format(ord(x), 'b')for x in rcv))
    #f = open('test.txt','w')
    #f.close
