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

srv_rtt_data = []
srv_rtt_date_time = []
rtt_data = []
rtt_list = []
rtt_date = []
all_rtt_data = []
cl_rtt_data = []

#x-label
label = []      
avgs = []       
dates= []
tup = ()

fig = plt.figure() #figsize=(40,70)
#search hierachy of folders
dirs = os.listdir( thedir )

k = 9
j = 1
m = 0
n = 3

fig = plt.figure(figsize=(15,35)) 
fig.subplots_adjust(hspace=0.7)   

for root_dirs in dirs:

	if root_dirs in 'client':	
		path = thedir+'/'+ root_dirs
		for root, dirs, files in os.walk(path):
						
			dirs.sort(reverse=True)
				
			if len(dirs) >= 7:
				dirs_arrange=dirs[0:3]
			else:			
				dirs_arrange=dirs[0:len(dirs)]
			
			for dirName in dirs_arrange:
				subdirpath = os.path.join(path, dirName)
				t = datetime.datetime.strptime(dirName , "%Y-%m-%d")
				
				if  datetime.datetime.today() > t:
					print 'true'
				else:
					print 'false'
				
				for subroot, subdirs, subfiles in os.walk(subdirpath):
					print 'subroot', subroot
				
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
						elif not data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]:
							continue
						elif data["result"]["timestamp"] is None:
							continue
						elif data["result"]["network"]["measr"]["nat"]is None:
							continue
						elif data["result"]["network"]["measr"]["nat"]["mapping"]is None:	
							continue
						elif not data["result"]["network"]["measr"]["nat"]["mapping"]:
							continue
						elif data["result"]["network"]["measr"]["nat"]["mapping"]["tcp"]is None:	
							continue
						elif data["result"]["network"]["measr"]["nat"]["mapping"]["tcp"]["pubip"]is None:	
							continue	
		                			
						latency_data=data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]
						timestamp_data=data["result"]["timestamp"]
						
						ip_data=data["result"]["network"]["measr"]["nat"]["mapping"]["tcp"]["pubip"][0]
											
						tup=(latency_data , timestamp_data, datetime.datetime.fromtimestamp(timestamp_data).strftime('%H:%M'), numpy.average(latency_data),ip_data)
						
						rtt_data.append(tup)
						
										
					if len(rtt_data) == 0:
						continue

					sorted_rtt_data = sorted(rtt_data, key=itemgetter(1))
		        		
					for i in sorted_rtt_data:
						if i[2] in label:
							continue
						rtt_list.append( i[0] )
						avgs.append( i[3] )
						label.append( i[2] )
						
		                	#print rtt_data
		                	print 'j: ',j
					ax1 = fig.add_subplot(k,1,j)
					ax1.set_title( dirName + ' clinet latency data boxplot' )
			 		ax1.set_xlabel('Hour')
			 		ax1.set_ylabel('rtt_ms')
					pylab.xticks(range(0,len(label)),label, rotation='vertical')
					ax1.boxplot(rtt_list)		                        
											
					rtt_date.append(numpy.average(avgs))
														
					ax2 = fig.add_subplot(k,1,j+1,axisbg='grey')
					ax2.set_title( dirName + ' clinet latency data time series plot' )
			 		ax2.set_xlabel('Hour')
			 		ax2.set_ylabel('rtt_ms')
			 		j = j + 3
			 		print 'dirs_arrange', dirs_arrange
					pylab.xticks(range(0,len(label)),label, rotation='vertical')
					#data.append(dirs_arrange)
					ax2.plot( avgs)
					
				all_rtt_data.append(sorted_rtt_data)
									
				rtt_data = []
				rtt_list = []
				avgs = []
				label = []
					
	                                                                                                          
	                                                                                                          
							                                                          
       	if root_dirs in 'server':
       		
       		#print 'all_rtt_data: ', all_rtt_data
       		path = thedir+'/'+ root_dirs               
       		for root, ser_dirs, files in os.walk(path):                                                           
			print >> sys.stderr, len(ser_dirs)
						
	       		ser_dirs.sort(reverse=True)                                                                   
	       		if len(ser_dirs) >= 3:                  
	       			srv_dirs_arrange=ser_dirs[0:3]                                                            
	       		else:	
	       			srv_dirs_arrange=ser_dirs[0:len(ser_dirs)]                                                    
	       			
	       	        print 'dirs_arrange', srv_dirs_arrange                                                                                        
	       		for dirName in srv_dirs_arrange:   
	       			                                                            
	       			subdirpath = os.path.join(path, dirName)     
	       			j = j+1                                     
	       			for subroot, subdirs, subfiles in os.walk(subdirpath):                            
	       				print 'dirName', dirName                                                  
	       				subdirs.sort(reverse=True)   
	       				print dirName                                             
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
	       					elif data["latency"] is None:
	       						continue
	       					elif data["latency"][0]["target_ip"] is None:
	       						continue
	       					elif data["latency"][0]["rtt_ms"] is None:
	       						contine
	       					elif not data["latency"][0]["rtt_ms"] :
	       						continue
	       					elif data["timestamp"] is None:
	       						continue
	       						
	       					srv_latency_data = data["latency"][0]["rtt_ms"] 
	       					timestamp_data=data["timestamp"]
	       					srv_ip_data = data["latency"][0]["target_ip"]
	       					tup = [srv_latency_data,timestamp_data,datetime.datetime.fromtimestamp(timestamp_data).strftime('%H:%M'), numpy.average(srv_latency_data),srv_ip_data]
	       					srv_rtt_data.append(tup)
	       					
	       					sorted_srv_rtt_data = sorted(srv_rtt_data, key=itemgetter(1))
	       					       					
	       	                 	aa = 0
	       	                 	
	       	                 		       	                 		       	                 	
	       	                 	if m < len(all_rtt_data) :
	      					
	       	                		for i in range(len(sorted_srv_rtt_data)):
	       	                	
	       	                			if aa >= len(all_rtt_data[m]):
	       	                				break
							       	                 			
	       	                 			while True:
	       	                 				
	       	                 				if aa < len(all_rtt_data[m]):
	       	                 							
	       	                 					if sorted_srv_rtt_data[i][1] < all_rtt_data[m][aa][1]:
	       	                 						break
	       	                 						
	       	                 				        if (sorted_srv_rtt_data[i][1] - all_rtt_data[m][aa][1] < 10) & (sorted_srv_rtt_data [i][4] == all_rtt_data[m][aa][4]):              
	       	                 				        	print "all_rtt_data[m][aa][3]", sorted_srv_rtt_data[i][1],' ',all_rtt_data[m][aa][1],' ',all_rtt_data[m][aa][3]
	       	                 				        	rtt_list.append( sorted_srv_rtt_data[i][0] )
	       	                 						avgs.append( sorted_srv_rtt_data[i][3] )
	       	                 						label.append( sorted_srv_rtt_data[i][2] )
	       	                 						cl_rtt_data.append(all_rtt_data[m][aa][3])
	       	                 						
	       	                 					aa+=1	
	       	                 				
	       	                 				
	       	                 				else:
	       	                 					break
						                					
	       	                 	m=m+1	
	       	                         	
	       	                       	ax3 = fig.add_subplot(k,1,n)
	       	                       	ax4 = fig.add_subplot(k,1,n)
	       				ax3.set_title( dirName +' server response clinet latency data time series plot (IP & Time match)' )
	       				ax3.set_xlabel('Hour')
	       				ax3.set_ylabel('rtt_ms')
	       				
	       				pylab.xticks(range(0,len(label)),label, rotation='vertical')
	       				
	       				ax3, = plt.plot(avgs, label = 'match')
	       			       	ax4, = plt.plot(cl_rtt_data, label = 'client')
	       			       	l1 = plt.legend([ax3], ["server"], loc=1)
					l2 = plt.legend([ax4], ["client"], loc=2) 
					plt.gca().add_artist(l1) 
					plt.gca().add_artist(l2)
	       	                       	
	       	                       	rtt_data = []
	       				rtt_list = []
	       				avgs = []
	       				label = []
	       				cl_rtt_data = []
	       				n = n+3	
	
				
			
plt.show()
