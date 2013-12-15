import os
import json
import numpy
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
matplotlib.pyplot.switch_backend('agg')
import datetime
import pylab
from operator import itemgetter
#import networkx as nx
#import web, sys
from PIL import Image, ImageDraw, ImageFont
import StringIO
import sys
import cStringIO


def application(environ, start_response):

	text = "rtt_ms"
	#data path
	thedir = '/srv/www/data/client/'
		
	rtt_data = []
	rtt_list = []
	rtt_date_time = []
	 
	#x-label
	label = []
	avgs = []
	dates= []
	tup = ()

	fig = plt.figure(figsize=(15,35))
	fig.subplots_adjust(hspace=0.7)
	
	skip = 0
	skip1 = 0
	#search hierachy of folders
	for root, dirs, files in os.walk(thedir):
		print >> sys.stderr, len(dirs)
		k = len(dirs) + 1
		j = 1
		dirs.sort(reverse=True)
		if len(dirs) >= 7:
			dirs_arrange=dirs[0:7]
		else:			
			dirs_arrange=dirs[0:len(dirs)]
		
			
		for dirName in dirs_arrange:
			
			#if skip % 2 == 1:
			#	skip=skip+1
			#	continue
			#skip = skip + 1
			
			subdirpath = os.path.join(root, dirName)
			for subroot, subdirs, subfiles in os.walk(subdirpath):
				for file in subfiles:
					if file.startswith('.'):
						continue
					if skip1 % 2 == 1:
						skip1 = skip1 + 1
						continue
					skip1 = skip1 + 1
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
					elif not data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]:
						continue
					elif data["result"]["timestamp"] is None:
						continue	
					
					latency_data=data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]
					timestamp_data=data["result"]["timestamp"]
					if latency_data is None:
						print 'None'
						continue
					tup=(latency_data , timestamp_data, datetime.datetime.fromtimestamp(timestamp_data).strftime('%H:%M'), numpy.average(numpy.average(latency_data)))
					rtt_data.append(tup)
					
				if len(rtt_data) == 0:
					continue
				
				sorted_rtt_data = sorted(rtt_data, key=itemgetter(1))
	        		
				for i in sorted_rtt_data:
					#tup=(i[1],i[2])
					rtt_list.append( i[0] )
					avgs.append( i[3] )
					label.append( i[2] )
				
				#print rtt_data
				ax1 = fig.add_subplot(k,1,j)
				ax1.set_title( dirName + ' latency data boxplot' )
	 			ax1.set_xlabel('Hour')
	 			ax1.set_ylabel('rtt_ms')
				pylab.xticks(range(0,len(label) - 1),label)
				ax1.boxplot(rtt_list)
	 		
	 		
	 		rtt_date_time.append(numpy.average(avgs))  	
	 		
       
			ax2 = fig.add_subplot(k,1,k,axisbg='grey')
			ax2.set_title( 'Latency data time series plot' )
	 		ax2.set_xlabel('Date')
	 		ax2.set_ylabel('rtt_ms')
			j = j + 2
			pylab.xticks(range(0,len(dirs_arrange) + 1),dirs_arrange)
			ax2.plot( rtt_date_time )
			
			rtt_data = []
			rtt_list = []
			avgs = []
			label = []
	
	format = 'png'
	sio = cStringIO.StringIO()
	plt.savefig( sio,format="png")
	
	status = '200 OK'
	headers = [('Content-type', 'image/png')]
	start_response(status, headers)
	
	print >> sys.stderr, "Until here is OK"
	
	return [sio.getvalue()]