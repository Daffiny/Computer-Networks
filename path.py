import os
import json
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pylab
from operator import itemgetter
#import networkx as nx
import Image
import sys
#matplotlib.use('Agg')

text = "rtt_ms"
#data path
thedir = 'D:/TUM/test_data'

rtt_data = []
rtt_list = []

#x-label
label = []
avgs = []
dates= []
tup = ()

fig = plt.figure(figsize=(40,70))
#search hierachy of folders
for root, dirs, files in os.walk(thedir):
	print >> sys.stderr, len(dirs)
	k = len(dirs) * 2
	j = 1

	for dirName in dirs:
		subdirpath = os.path.join(root, dirName)
		for subroot, subdirs, subfiles in os.walk(subdirpath, topdown=True):
				print subroot
				subdirs.sort(reverse=True)
				for file in subfiles:					
				
					if file.startswith('.'):
						continue
                
					filepath = os.path.join(subroot, file)
					json_data = open(filepath)
                
					# search the below data of rtt_ms
					data = json.load(json_data)
					json_data.close()
                
					if data is None:
						continue
					elif data["result"] is None:
						continue
					elif data["result"]["network"] is None:
						contine
					elif data["result"]["network"]["measr"] is None:
						continue
					elif data["result"]["network"]["measr"]["latency"] is None:
						continue
					elif data["result"]["network"]["measr"]["latency"][0] is None:
						continue
					elif data["result"]["network"]["measr"]["latency"][0]["rtt_ms"] is None:
						continue
					elif data["result"]["timestamp"] is None:
						continue
                
					latency_data=data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]
					timestamp_data=data["result"]["timestamp"]
					tup=(latency_data , timestamp_data, datetime.datetime.fromtimestamp(timestamp_data).strftime('%H:%M'), numpy.average(latency_data))
					rtt_data.append(tup)
                
				if len(rtt_data) == 0:
					continue
                
				sorted_rtt_data = sorted(rtt_data, key=itemgetter(1))
        
				#for i in sorted_rtt_data:
				#	#tup=(i[1],i[2])
				#	rtt_list.append( i[0] )
				#	avgs.append( i[3] )
				#	label.append( i[2] )
                		#	#print rtt_data
				#	ax1 = fig.add_subplot(k,1,j)
				#	ax1.set_title( dirName + ' latency data boxplot' )
	 			#	ax1.set_xlabel('Hour')
	 			#	ax1.set_ylabel('rtt_ms')
				#	pylab.xticks(range(0,len(label) - 1),label)
				#	ax1.boxplot(rtt_list)
                        	#
				#	ax2 = fig.add_subplot(k,1,j + 1)
				#	ax2.set_title( dirName + ' latency data time series plot' )
	 			#	ax2.set_xlabel('Hour')
	 			#	ax2.set_ylabel('rtt_ms')
				#j = j + 2
				#pylab.xticks(range(0,len(label) - 1),label)
				#ax2.plot( avgs )
				#rtt_data = []
				#rtt_list = []
				#avgs = []
				#label = []

#plt.show()

