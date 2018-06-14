import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys
sys.path.append('..')

from datetime import datetime as dt
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import os
import inquirer
from utils import utils

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
#ax2 = fig.add_subplot(4,1,2)
ax3 = fig.add_subplot(3,1,2)
ax4 = fig.add_subplot(3,1,3)

datadir = "data/"
datafile = utils.newest(datadir)

accept_newest = utils.query_yn("\nPlotting the most recent datafile in the data folder:\n	" +
			 str(datafile) +
			 "\nIs this okay?",
			 default = "yes")

if accept_newest == True:
	datafile = datafile
else:
	question = [
		inquirer.List('altfile',
		message = "Which file do you then want to plot?",
		choices = paths,
		),
	]
	answer = inquirer.prompt(question)
	datafile = answer["altfile"]
def mkFig(i):
	with open(datafile,"r") as lines:
		next(lines)
		time_data = []
		pO2_data = []
		pCO2_data = []
		power_data = []
		probeTemp_data = []
		count = 0
		for line in lines:
			if len(line) > 1:
				count+=1
				time, pO2, pCO2, power, probeTemp = line.split(";")
				time_data.append(dt.strptime(time, '%d/%m-%Y %H:%M:%S'))

				try:
					pO2_data.append(float(pO2))
				except ValueError:
					pO2_data.append(np.NaN)

				try:
					pCO2_data.append(float(pCO2))
				except ValueError:
					pCO2_data.append(np.NaN)

				try:
					power_data.append(int(power))
				except ValueError:
					power_data.append(np.NaN)

				try:
					probeTemp_data.append(float(probeTemp))
				except ValueError:
					probeTemp_data.append(np.NaN)

		pd_datetime = pd.to_datetime(time_data)

		df = pd.DataFrame({"pO2": pO2_data, "pCO2": pCO2_data, "power": power_data,
		"probeTemp": probeTemp_data},
		index = pd_datetime,
		columns = ['pO2', 'pCO2', 'power', 'probeTemp'])

		df_min = df 
		#df_min = df.resample("1min").mean()

		ax1.clear()
		#ax2.clear()
		ax3.clear()
		ax4.clear()
		ax1.plot(df_min.index.to_pydatetime(), df_min['pO2'], label="$pO_2$", color="r")
		ax1.plot(df_min.index.to_pydatetime(), df_min['pCO2'], label="$pCO_2$", color="b")
		ax3.plot(df_min.index.to_pydatetime(), df_min['power'])
		ax4.plot(df_min.index.to_pydatetime(), df_min['probeTemp'])
		ax1.legend(loc=1)
		#
		#ax1.set_ylim(95, 101)
		#ax1.set_ylim(ax1.get_ylim()[0], 101)
		#ax1.set_ylim(ax1.get_ylim()[0], ax1.get_ylim()[1])
		ax1.set_ylabel("mmHg")
		
		#ax2.set_ylim(ax2.get_ylim()[0], 450)
		#ax2.set_ylim(ax2.get_ylim()[0], ax2.get_ylim()[1])
		#ax2.set_ylabel("pCO2 (mmHg)")

		#ax2.set_ylim(ax2.get_ylim()[0], 450)
		#ax2.set_ylim(ax2.get_ylim()[0], ax2.get_ylim()[1])
		ax3.set_ylabel("Probe (mW)")

		#ax2.set_ylim(ax2.get_ylim()[0], 450)
		#ax2.set_ylim(ax2.get_ylim()[0], ax2.get_ylim()[1])
		ax4.set_ylabel("Probe ($^\circ$C)")

		hours = mdates.HourLocator()   # every year
		timeFmt = mdates.DateFormatter('%H:%M')
		
		if(count<=(60/2)*15):
			minutes = mdates.MinuteLocator(interval=1)

			ax1.xaxis.set_major_locator(minutes)
			ax1.xaxis.set_major_formatter(timeFmt)

			#ax2.xaxis.set_major_locator(minutes)
			#ax2.xaxis.set_major_formatter(timeFmt)
			
			ax3.xaxis.set_major_locator(minutes)
			ax3.xaxis.set_major_formatter(timeFmt)
			
			ax4.xaxis.set_major_locator(minutes)
			ax4.xaxis.set_major_formatter(timeFmt)
		else:
			minutes = mdates.MinuteLocator(byminute=range(0,60,15))

			ax1.xaxis.set_major_locator(hours)
			ax1.xaxis.set_major_formatter(timeFmt)
			ax1.xaxis.set_minor_locator(minutes)

			#ax2.xaxis.set_major_locator(hours)
			#ax2.xaxis.set_major_formatter(timeFmt)
			#ax2.xaxis.set_minor_locator(minutes)

			ax3.xaxis.set_major_locator(hours)
			ax3.xaxis.set_major_formatter(timeFmt)
			ax3.xaxis.set_minor_locator(minutes)

			ax4.xaxis.set_major_locator(hours)
			ax4.xaxis.set_major_formatter(timeFmt)
			ax4.xaxis.set_minor_locator(minutes)

		ax1.annotate("pO2: " + pO2, xy=(1, 0.6), xytext=(8, 0), 
		xycoords=('axes fraction'), textcoords='offset points')
		
		ax1.annotate("pCO2: " + pCO2, xy=(1, 0.4), xytext=(8, 0), 
		xycoords=('axes fraction'), textcoords='offset points')
		
		ax3.annotate(power, xy=(1, 0.5), xytext=(8, 0), 
		xycoords=('axes fraction'), textcoords='offset points')

		ax4.annotate(probeTemp, xy=(1, 0.5), xytext=(8, 0), 
		xycoords=('axes fraction'), textcoords='offset points')

fig.suptitle("Biometric values from Radiometer")
plt.figtext(0.5, .9, datafile, ha='center', fontsize=9)
#fig.suptitle(datafile)
#fig.figtext(datafile)

liveplot = anim.FuncAnimation(fig, mkFig, interval=1000)

plt.show()
