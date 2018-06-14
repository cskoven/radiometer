import serial
import time
from datetime import datetime
import io
import os
import numpy as np

usbdev_linux = "/dev/ttyUSB0"
usbdev_mac = "/dev/tty.usbserial-AI03GF6T"

#mmHg2kPa = 133.322387415

if os.path.exists(usbdev_linux):
	usbdev = usbdev_linux
elif os.path.exists(usbdev_mac):
	usbdev = usbdev_mac

ser = serial.Serial(usbdev, 9600, timeout=2)  # open serial port

sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
sio.flush() # it is buffering. required to get the data out *now*

file_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")	
outfile='data/radiometer_' + file_suffix + '.csv'
print("\n", "Data file: ", outfile, end="\n\n")

with open(outfile,'a+') as f: #appends to existing file
	header = "datetime" + ";" + "pO2" + ";" + "pCO2" + ";" + "Power" + ";" + "probeTemp" + '\n'
	print(header, end="")

	f.write(header)
	f.flush()
		
	while ser.isOpen():
		datastring	= sio.readline()
		if((len(datastring))<=1):
			print("Waiting 2sec to get data")
			time.sleep(2)
		else:
			time, pO2, pCO2, power, probeTemp = datastring.split(";")
			pO2_k, pO2, pO2_u = pO2.split()
			pCO2_k, pCO2, pCO2_u = pCO2.split()
			power_k, power, power_u = power.split()
			probeTemp_k, probeTemp, probeTemp_u = probeTemp.split()
		#pO2		= datastring[14:17].strip()
		#pCO2		= datastring[28:32].strip()
		#power		= datastring[45:49].strip()
		#probeTemp	= datastring[60:64].strip()
		
		#SpO2 = datastring[5:8].strip()
		#HR = datastring[12:15].strip()
		
			now = datetime.now().strftime("%d/%m-%Y %H:%M:%S")
			dataline = now + ";" + pO2 + ";" + pCO2 + ";" + power + ";" + probeTemp + "\n"
			#dataline = now + ";" + datastring + "\n" 

			print(dataline, end="")
			f.write(dataline)
			f.flush()

ser.close()             #close port
