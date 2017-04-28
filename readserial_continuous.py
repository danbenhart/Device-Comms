#!/usr/bin/env python

'''
This version of the readserial program demonstrates using python to write 
an output file
'''
import time
from datetime import datetime
import serial
import csv
import binascii

outfile = "C:\\Users\\benhartd\\Desktop\\serial_log.csv"

ser = serial.Serial(
   port='COM4',
)

i = 0
timelimit = 5
starttime = time.time()

print(str(ser.is_open))

data = ''
max_thickness = 0
max_thickness_loc = []

with open(outfile, 'w', newline='')as f:  # appends to existing file
    writerobject = csv.writer(f)
    while ser.isOpen() and (time.time() < starttime + timelimit):
        # print("TP2")
        ser.write(b'A\r\n')
        datastring = ser.readline()
        # print("TP3")
        xval = float(str(datastring.split(b',')[0], 'UTF8')[2:])
        yval = float(str(datastring.split(b',')[1], 'UTF8')[2:])
        if xval > max_thickness:
            max_thickness = xval
            max_thickness_loc = [xval, yval]
        writerobject.writerow([datetime.utcnow().isoformat(), xval, yval])

        f.flush()  # included to force the system to write to disk
        i += 1
        # time.sleep(.05)
    writerobject.writerow(["Max Thickness", max_thickness_loc[0], max_thickness_loc[1]])
ser.close()
print(i)

