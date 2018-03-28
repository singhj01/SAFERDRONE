#!/usr/bin/env python 
import serial
import time
#Define UART Port
#1 startbit, 8 databits, 1 odd parity, 2 stopbits
port = serial.Serial('/dev/ttyAMA0')
#port.baudrate = 100000
#port.bytesize = 8
#port.parity = serial.PARITY_ODD
#port.stopbits = 2
#port.timeout = 6


port.write("hello")
rcv = port.read(5)
print(rcv)
