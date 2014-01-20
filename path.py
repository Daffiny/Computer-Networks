import os
import json
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pylab
from operator import itemgetter
import scipy
from scipy.stats import pearsonr
#import networkx as nx
import Image
import sys
#matplotlib.use('Agg')

def main():
    print "main"
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
    week_date = []
    week_plot_data = []
    power_list = []
    celsius_list = []
    ram_list = []
    speed_list = []
    
    #x-label
    label = []      
    avgs = []       
    dates= []
    tup = ()
    
    fig = plt.figure() #figsize=(40,70)
    #search hierachy of folders
    dirs = os.listdir( thedir )
    
    k = 8
    j = 1
    m = 0
    n = 3
    
    fig = plt.figure(figsize=(50,70)) 
    fig.subplots_adjust(hspace=0.7)   
    
    for root_dirs in dirs:
    
        if root_dirs in 'client':    
            path = thedir+'/'+ root_dirs
            for root, dirs, files in os.walk(path):
                            
                dirs.sort(reverse=True)
                    
                if len(dirs) >= 7:
                    dirs_arrange=dirs[0:7]
                else:            
                    dirs_arrange=dirs[0:len(dirs)]
                
                for dirName in dirs_arrange:
                   
                    subdirpath = os.path.join(path, dirName)
    #                t = datetime.datetime.strptime(dirName , "%Y-%m-%d")
                    
                    for subroot, subdirs, subfiles in os.walk(subdirpath):
            
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
                                continue
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
                                                        
                             # Wifi
                            type =  data["result"]["network"]["type"]         
                            if type in 'WIFI':
                                if data["result"]["network"]["wifi"] is None:
                                    continue
                                elif data["result"]["network"]["wifi"]["current"] is None:
                                    continue
                                elif data["result"]["network"]["wifi"]["current"]["speed_mbps"] is None:
                                    continue
                                speed = data["result"]["network"]["wifi"]["current"]["speed_mbps"]
                            else:
                                speed = 0  
                            
                            #battery
                            power = data["result"]["status"]["battery"]["level"]
                            celsius = data["result"]["status"]["battery"]["celsius"]
                            
                            #RAM
                            ram = data["result"]["status"]["usage"]["ramfree_mb"]
                            
                            #Magnetic
                            magnetic = data
                            
                            
                            latency_data=data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]
                            timestamp_data=data["result"]["timestamp"]
                            
                            ip_data=data["result"]["network"]["measr"]["nat"]["mapping"]["tcp"]["pubip"][0]
                                                
                            tup=(latency_data , timestamp_data, datetime.datetime.fromtimestamp(timestamp_data).strftime('%d/%m %H:%M'), 
                                 numpy.average(latency_data),ip_data,power,celsius,ram,speed)
                            
                            rtt_data.append(tup)
                           
                        if len(rtt_data) == 0:
                            continue
    
                        sorted_rtt_data = sorted(rtt_data, key=itemgetter(1))
                        
        #Record the plot data each day in 7 days
        for i in sorted_rtt_data:
            if i[2] in label:
                continue
            rtt_list.append( i[0] )
            avgs.append( i[3] )
            label.append( i[2] )
            power_list.append(i[5])
            celsius_list.append(i[6])
            ram_list.append(i[7])
            speed_list.append(i[8])
               
        # pearson coefficient
        a,power_list_value = pearsonr(avgs, power_list)
        a,celsius_list_value = pearsonr(avgs, celsius_list)
        a,ram_list_value = pearsonr(avgs, ram_list)
        a,speed_list_value = pearsonr(avgs, speed_list)
        print power_list_value,' ',celsius_list_value,' ',ram_list_value,' ',speed_list_value

        #print rtt_data
        ax1 = fig.add_subplot(k,1,1)
        ax1.set_title( ' Weekly clinet latency data boxplot' )
        ax1.set_xlabel('Hour')
        ax1.set_ylabel('rtt_ms')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax1.boxplot(rtt_list)
        
        ax2 = fig.add_subplot(k,1,2)
        ax2.set_title('Weekly clinet latency data time series plot' )
        ax2.set_xlabel('Hour')
        ax2.set_ylabel('rtt_ms')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax2.plot( avgs)
               
        ax5 = fig.add_subplot(k,1,4)
        ax5.set_title('Weekly Power data time series plot' )
        ax5.set_xlabel('Time')
        ax5.set_ylabel('Battery Level (%)')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax5t = 'pearson coefficient = ',power_list_value
        ax5.annotate(ax5t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
                ha='right', va='bottom')
        ax5.plot( power_list)
        
        ax6 = fig.add_subplot(k,1,5)
        ax6.set_title('Weekly Temperature data time series plot' )
        ax6.set_xlabel('Time')
        ax6.set_ylabel('Battery Temperature (C)')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax6t = 'pearson coefficient = ',celsius_list_value
        ax6.annotate(ax6t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
                ha='right', va='bottom')
        ax6.plot( celsius_list)
        
        ax7 = fig.add_subplot(k,1,6)
        ax7.set_title('Weekly RAM data time series plot' )
        ax7.set_xlabel('Time')
        ax7.set_ylabel('Free RAM (MB)')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax7t = 'pearson coefficient = ',ram_list_value
        ax7.annotate(ax7t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
                ha='right', va='bottom')
        ax7.plot( ram_list)
        
        ax8 = fig.add_subplot(k,1,7)
        ax8.set_title('Weekly Wifi Speed data time series plot' )
        ax8.set_xlabel('Time')
        ax8.set_ylabel('Wifi Speed (Mbps)')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax8t = 'pearson coefficient = ',speed_list_value
        ax8.annotate(ax8t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
                ha='right', va='bottom')
        ax8.plot( speed_list)
                        
        ax9 = fig.add_subplot(k,1,8)
        ax10 = fig.add_subplot(k,1,8)
        ax9.set_title( 'Battery level  V.S RAM' )
        ax9.set_xlabel('Time ')
        ax9.set_ylabel('% & MB')                               
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax9, = plt.plot(power_list, label = 'match')
        ax10, = plt.plot(ram_list, label = 'client')
        l1 = plt.legend([ax9], ["Battery"], loc=1)
        l2 = plt.legend([ax10], ["RAM"], loc=2) 
        
        all_rtt_data.append(sorted_rtt_data)
                                        
        rtt_data = []
        rtt_list = []
        avgs = []
        label = []
        week_date = []
        week_plot_data = []
        power_list = []
        celsius_list = []
        ram_list = []
        speed_list = []
                                 
        #Data from Server folder                                                                                      
        if root_dirs in 'server':
            #print 'all_rtt_data: ', all_rtt_data
            path = thedir+'/'+ root_dirs               
            for root, ser_dirs, files in os.walk(path):                                                           
    
                ser_dirs.sort(reverse=True)                                                                   
                if len(ser_dirs) >= 3:                  
                    srv_dirs_arrange=ser_dirs[0:7]                                                            
                else:    
                    srv_dirs_arrange=ser_dirs[0:len(ser_dirs)]                                                    
    
                for dirName in srv_dirs_arrange:   
                                                                                       
                    subdirpath = os.path.join(path, dirName)     
                    j = j+1                                     
                    for subroot, subdirs, subfiles in os.walk(subdirpath):                            
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
                            elif data["latency"] is None:
                                continue
                            elif data["latency"][0]["target_ip"] is None:
                                continue
                            elif data["latency"][0]["rtt_ms"] is None:
                                continue
                            elif not data["latency"][0]["rtt_ms"] :
                                continue
                            elif data["timestamp"] is None:
                                continue
                                       
                            srv_latency_data = data["latency"][0]["rtt_ms"] 
                            timestamp_data=data["timestamp"]
                            srv_ip_data = data["latency"][0]["target_ip"]
                            tup = [srv_latency_data,timestamp_data,datetime.datetime.fromtimestamp(timestamp_data).strftime('%d/%m %H:%M'), numpy.average(srv_latency_data),srv_ip_data]
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
                                                                
                                            rtt_list.append( sorted_srv_rtt_data[i][0] )
                                            avgs.append( sorted_srv_rtt_data[i][3] )
                                            label.append( sorted_srv_rtt_data[i][2] )
                                            cl_rtt_data.append(all_rtt_data[m][aa][3])
                                                            
                                        aa+=1    
                                    else:
                                        break
                                                                
                        m=m+1    
                                                
        ax3 = fig.add_subplot(k,1,3)
        ax4 = fig.add_subplot(k,1,3)
        ax3.set_title( dirName +' server response clinet latency data time series plot (IP & Time match)' )
        ax3.set_xlabel('Hour')
        ax3.set_ylabel('rtt_ms')
                               
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
                               
        ax3, = plt.plot(avgs, label = 'match')
        ax4, = plt.plot(cl_rtt_data, label = 'client')
        l1 = plt.legend([ax3], ["server"], loc=1)
        l2 = plt.legend([ax4], ["client"], loc=2) 
        #plt.gca().add_artist(l1) 
        #plt.gca().add_artist(l2)
                                              
        rtt_data = []
        rtt_list = []
        avgs = []
        label = []
        cl_rtt_data = []
        n = n+3    
        
                    
                
    plt.show()

if __name__ == '__main__':
    main()
    pass