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
import Image
import sys
import timeit
#import LevenshteinDistance

start = timeit.timeit();

def main():
    
    #from __future__ import division
    def LevenshteinDistance( a, b ):
        len_a = len(a)
        len_b = len(b)
        x = [[0 for y_axis in range(len_b)] for x_axis in range(len_a)]
        
        for i in range( len_a ):
            x[i][0] = i
        
        for j in range( len_b ):
            x[0][j] = j
            
        for j in range( 1, len_b ):
            for i in range( 1, len_a ):
                if a[i] == b[j]:
                    x[i][j] = x[ i - 1][j - 1]
                else:
                    x[i][j] = min( x[i-1][j] + 1, x[i][j-1] + 1, x[i-1][ j-1] + 1 )
        
        return x[ len_a - 1][len_b - 1 ]
    
    def LevenshteinDistance_for_ip( a, b ):
        len_a = len(a)
        len_b = len(b)
        
        x = [[0 for y_axis in range(len_b)] for x_axis in range(len_a)]
        
        for i in range( len_a ):
            x[i][0] = i
        
        for j in range( len_b ):
            x[0][j] = j
            
        for j in range( 1, len_b ):
            for i in range( 1, len_a ):
                if a[i][0:a[i].rfind('.')] == b[j][0:b[j].rfind('.')]:
                    x[i][j] = x[ i - 1][j - 1]
                else:
                    x[i][j] = min( x[i-1][j] + 1, x[i][j-1] + 1, x[i-1][ j-1] + 1 )
        
        return x[ len_a - 1][len_b - 1 ]

    text = "rtt_ms"
    #data path
    thedir = 'D:/TUM/test_data'
    
    srv_rtt_data = []
    rtt_data = []
    rtt_data_100 = []
    rtt_list = []
    all_rtt_data = []
    cl_rtt_data = []
    power_list = []
    celsius_list = []
    ram_list = []
    speed_list = []
    avg_value = []
    ssid_eduroam_list = []
    ssid_others_list = []
    signal_list = []
    magnetic_list = []
    
    #x-label
    label = []      
    avgs = []       
    dates= []
    tup = ()
    
    fig = plt.figure() #figsize=(40,70)
    #search hierachy of folders
    dirs = os.listdir( thedir )
    
    #total number of graph on the same plot 
    k = 16
    m = 0
    n = 3
    p = 0
    j = 0
    
    fig = plt.figure(figsize=(50,70)) 
    fig.subplots_adjust(hspace=0.7) 
  #  fig, axes = plt.subplots(nrows=16, ncols=1)  
  #  fig.tight_layout( pad=1.5 )

    #fig.tight_layout(h_pad=1)
    path = thedir+'/'+ 'client'
    for root, dirs, files in os.walk(path):
    
    #for root_dirs in dirs:
    
        #if root_dirs in 'client':    
            #path = thedir+'/'+ root_dirs
            #for root, dirs, files in os.walk(path):
                            
                dirs.sort(reverse=True)
                
                if len(dirs) >= 3:
                    dirs_arrange=dirs[0:3]
                else:            
                    dirs_arrange=dirs[0:len(dirs)]
                
                
                #dirs_arrange = dirs[6:9]
                
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
                            elif not data["result"]:
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
                            elif data["result"]["status"] is None:
                                continue
                            elif data["result"]["status"]["battery"] is None:
                                continue
                            elif data["result"]["status"]["battery"]["level"] is None:
                                continue
                            elif data["result"]["status"]["battery"]["celsius"] is None:
                                continue
                            elif data["result"]["status"]["usage"] is None:
                                continue
                            elif data["result"]["status"]["usage"]["ramfree_mb"] is None:
                                continue
                            #added by derek
                            elif data["result"]["network"]["measr"]["traceroute"] is None:
                                continue
                            elif data["result"]["network"]["measr"]["traceroute"][0]["hops"] is None:
                                continue
                            ####
                            
                                                        
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
                                #ssid
                                if data["result"]["network"]["wifi"]["current"]["ssid"] is None:
                                    continue
                                ssid = data["result"]["network"]["wifi"]["current"]["ssid"]
                                if ssid == 'eduroam':
                                    ssid_eduroam = speed
                                    ssid_others = 0
                                else:
                                    ssid_others = speed
                                    ssid_eduroam = 0
                                #Signal    
                                if data["result"]["network"]["wifi"]["current"]["signal"] is None:
                                    continue
                                signal =  data["result"]["network"]["wifi"]["current"]["signal"]
                                
                            else:
                                speed = 0 
                                ssid_eduroam = 0 
                                ssid_others = 0
                                signal = 0
                            
                            #battery
                            power = data["result"]["status"]["battery"]["level"]
                            celsius = data["result"]["status"]["battery"]["celsius"]
                            
                            #RAM
                            ram = data["result"]["status"]["usage"]["ramfree_mb"]
                            
                            latency_data=data["result"]["network"]["measr"]["latency"][0]["rtt_ms"]
                            timestamp_data=data["result"]["timestamp"]
                            
                            #magnetic_field
                            if data["result"]["environment"]["magnetic_field"] is None:
                                continue
                            elif data["result"]["environment"]["magnetic_field"]["pow_mA"] is None:
                                continue
                            magnetic = data["result"]["environment"]["magnetic_field"]["pow_mA"]    
                                
                            #added by derek
                            trauceroute_AS = []
                            trauceroute_IP = []
                            trauceroute_hop = data["result"]["network"]["measr"]["traceroute"][0]["hops"]
                            
                            for x in trauceroute_hop:
                                if x["as"] is None:
                                    continue
                                if x["as"][0] == 'AS12816/AS680/AS1275': x["as"][0] = x["as"][0][0:7]
                                if x["as"][0] not in trauceroute_AS and x["as"][0] != '*':  trauceroute_AS.append(x["as"][0])
                                if x["ip"][0] != '192.168.1.1': trauceroute_IP.append(x["ip"][0])
                            ####
                            
                            ip_data=data["result"]["network"]["measr"]["nat"]["mapping"]["tcp"]["pubip"][0]
                                                
                            tup=(latency_data , 
                                 timestamp_data, 
                                 datetime.datetime.fromtimestamp(timestamp_data).strftime('%d %H:%M'), 
                                 numpy.average(latency_data),
                                 ip_data,
                                 power,
                                 celsius,
                                 ram,
                                 speed,
                                 ssid_eduroam,
                                 ssid_others,
                                 #added by derek
                                 trauceroute_AS, 
                                 trauceroute_IP,
                                 ####
                                 signal,
                                 magnetic
                                 )
                            
                            avg_value.extend(latency_data)
                            rtt_data.append(tup)
                           
                        if len(rtt_data) == 0:
                            continue
    
                        sorted_rtt_data = sorted(rtt_data, key=itemgetter(1))
        #end1 = timeit.timeit()
        #print "TIME1 =" , (end1-start);
             
    latency_data_avg = numpy.average(avg_value)
                 
        #Record the plot data each day in 7 days
        
        
    sorted_rtt_data = [list(t) for t in sorted_rtt_data]
    for i in range(len(sorted_rtt_data)):
        if sorted_rtt_data[i][2] in label:
            continue
        # remove extreme value
        temp1 = []
        for each in sorted_rtt_data[i][0]:
            if ((each < latency_data_avg*5) or (each < 1000)):
                temp1.append(each)  
            
        sorted_rtt_data[i][0] = temp1
        if len(sorted_rtt_data[i][0]) == 0:
            continue
                                           
        rtt_list.append(sorted_rtt_data[i][0] )
        avgs.append( numpy.average(sorted_rtt_data[i][0]) )
        label.append( sorted_rtt_data[i][2] )
        power_list.append(sorted_rtt_data[i][5])
        celsius_list.append(sorted_rtt_data[i][6])
        ram_list.append((float(2000-sorted_rtt_data[i][7])/2000)*100)
        speed_list.append(sorted_rtt_data[i][8])
        ssid_eduroam_list.append(sorted_rtt_data[i][9])
        ssid_others_list.append(sorted_rtt_data[i][10])
        signal_list.append(sorted_rtt_data[i][13])
        magnetic_list.append(sorted_rtt_data[i][14])
        rtt_data_100.append(float(numpy.average(sorted_rtt_data[i][0])/100))
               
        #end2 = timeit.timeit()
        #print "TIME2 =" , (end2-end1);end2=None;end1=None;
        
        # pearson coefficient
        

    power_list_value,a = pearsonr(avgs, power_list)
    celsius_list_value,b = pearsonr(avgs, celsius_list)
    ram_list_value,c = pearsonr(avgs, ram_list)
    speed_list_value,d = pearsonr(avgs, speed_list)
    signal_list_value,e = pearsonr(avgs, signal_list)
    magnetic_list_value,e = pearsonr(avgs, magnetic_list)
    
    #print rtt_data
    ax1 = fig.add_subplot(k,1,1)
    ax1.set_title( '3 days clinet latency data boxplot' )
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('rtt_ms')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    ax1.boxplot(rtt_list)
    
    ax2 = fig.add_subplot(k,1,2)
    #ax2.set_title('3 days clinet latency data time series plot' )
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('rtt_ms')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25,900, '3 days clinet latency data time series plot', fontsize=14, ha='left', va='top')
    ax2.plot( avgs,'ko-')
           
    ax5 = fig.add_subplot(k,1,4)
    #ax5.set_title('3 days Power data time series plot' )
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Battery Level (%)')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 100, '3 days Power data time series plot', fontsize=14, ha='left', va='top')
    ax5t = 'pearson coefficient = ',power_list_value
    ax5.annotate(ax5t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
            ha='right', va='bottom')
    ax5.plot( power_list,'ko-')
    
    ax6 = fig.add_subplot(k,1,5)
    #ax6.set_title('3 days Temperature data time series plot' )
    ax6.set_xlabel('Time')
    ax6.set_ylabel('Battery Temperature (C)')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 30, '3 days Temperature data time series plot', fontsize=14, ha='left', va='top')
    ax6t = 'pearson coefficient = ',celsius_list_value
    ax6.annotate(ax6t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
            ha='right', va='bottom')
    ax6.plot( celsius_list,'ko-')
    
    ax7 = fig.add_subplot(k,1,6)
   # ax7.set_title('3 days RAM data time series plot' )
    ax7.set_xlabel('Time')
    ax7.set_ylabel('Free RAM (MB)')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 90, '3 days RAM data time series plot', fontsize=14, ha='left', va='top')
    ax7t = 'pearson coefficient = ',ram_list_value
    ax7.annotate(ax7t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
            ha='right', va='bottom')
    ax7.plot( ram_list,'ko-')
    
    ax8 = fig.add_subplot(k,1,7)
    #ax8.set_title('3 days Wifi Speed data time series plot' )
    ax8.set_xlabel('Time')
    ax8.set_ylabel('Wifi Speed (Mbps)')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 70, '3 days Wifi Speed data time series plot', fontsize=14, ha='left', va='top')
    ax8t = 'pearson coefficient = ',speed_list_value
    ax8.annotate(ax8t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
            ha='right', va='bottom')
    ax8.plot( speed_list,'ko-')
                   
    ax9 = fig.add_subplot(k,1,8)
    ax10 = fig.add_subplot(k,1,8)
    #ax9.set_title( 'Battery level  V.S RAM' )
    ax9.set_xlabel('Time ')
    ax9.set_ylabel('%')                               
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 90, 'Battery level  V.S RAM', fontsize=14, ha='left', va='top')
    ax9, = plt.plot(power_list, label = 'match')
    ax10, = plt.plot(ram_list, label = 'client')
    l3 = plt.legend([ax9], ["Battery"], loc=1)
    l4 = plt.legend([ax10], ["RAM"], loc=2)
    plt.gca().add_artist(l3) 
    plt.gca().add_artist(l4)  
    
    ax11 = fig.add_subplot(k,1,9)
    ax12 = fig.add_subplot(k,1,9)
    #ax11.set_title( 'Wifi speed in different regional' )
    ax11.set_xlabel('Time ')
    ax11.set_ylabel('Wifi Speed (Mbps)')                               
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 70, 'Wifi speed in different regional' , fontsize=14, ha='left', va='top')
    ax11, = plt.plot(ssid_eduroam_list, label = 'match')
    ax12, = plt.plot(ssid_others_list, label = 'client')
    l5 = plt.legend([ax9], ["School"], loc=1)
    l6 = plt.legend([ax10], ["Home"], loc=2)
    plt.gca().add_artist(l5) 
    plt.gca().add_artist(l6)
    
    ax13 = fig.add_subplot(k,1,10)
    #ax13.set_title('3 days Signal data time series plot' )
    ax13.set_xlabel('Time')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 0, '3 days Signal data time series plot', fontsize=14,  ha='left', va='top')
    ax13t = 'pearson coefficient = ',signal_list_value
    ax13.annotate(ax13t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
            ha='right', va='bottom')
    ax13.plot(signal_list,'ko-')
    
    
    ax14 = fig.add_subplot(k,1,11)
   # ax14.set_title('3 days Magnetic data time series plot' )
    ax14.set_xlabel('Time')
    ax14.set_ylabel('mA')
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 60, '3 days Magnetic data time series plot' , fontsize=14,  ha='left', va='top')
    ax14t = 'pearson coefficient = ',magnetic_list_value
    ax14.annotate(ax14t, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
            ha='right', va='bottom')
    ax14.plot(magnetic_list,'ko-')
    
    
    ax15 = fig.add_subplot(k,1,12)
    ax16 = fig.add_subplot(k,1,12)
    #ax15.set_title( 'Clinet Latency VS Temperature' )
    ax15.set_xlabel('Time ')
    ax15.set_ylabel('rtt/100 VS C')                               
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 20, 'Clinet Latency VS Temperature' , fontsize=14, ha='left', va='top')
    ax15, = plt.plot(celsius_list, label = 'match')
    ax16, = plt.plot(rtt_data_100, label = 'client')
    l7 = plt.legend([ax15], ["Temperature"], loc=1)
    l8 = plt.legend([ax16], ["clinet latency"], loc=2)
    plt.gca().add_artist(l7) 
    plt.gca().add_artist(l8)
    
    ax17 = fig.add_subplot(k,1,13)
    ax18 = fig.add_subplot(k,1,13)
    #ax17.set_title( 'Clinet Latency VS RAM' )
    ax17.set_xlabel('Time ')
    ax17.set_ylabel('rtt/100 VS % ')                               
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 60, 'Clinet Latency VS RAM' , fontsize=14, ha='left', va='top')
    ax17, = plt.plot(ram_list, label = 'match')
    ax18, = plt.plot(rtt_data_100, label = 'client')
    l17 = plt.legend([ax17], ["RAM"], loc=1)
    l18 = plt.legend([ax18], ["clinet latency"], loc=2)
    plt.gca().add_artist(l17) 
    plt.gca().add_artist(l18)
    
    ax19 = fig.add_subplot(k,1,14)
    ax20 = fig.add_subplot(k,1,14)
    #ax19.set_title( 'Clinet Catency VS Baterry level' )
    ax19.set_xlabel('Time ')
    ax19.set_ylabel('rtt/100 VS % ')                               
    pylab.xticks(range(0,len(label)),label, rotation='vertical')
    plt.text(25, 60, 'Clinet Catency VS Baterry level' , fontsize=14, ha='left', va='top')
    ax19, = plt.plot(power_list, label = 'match')
    ax20, = plt.plot(rtt_data_100, label = 'client')
    l19 = plt.legend([ax19], ["Baterry level"], loc=1)
    l20 = plt.legend([ax20], ["clinet latency"], loc=2)
    plt.gca().add_artist(l19) 
    plt.gca().add_artist(l20)
    
    all_rtt_data.append(sorted_rtt_data)
                                    
    rtt_data = []
    rtt_list = []
    avgs = []
    label = []
    power_list = []
    celsius_list = []
    ram_list = []
    speed_list = []
    ssid_others_list = []
    ssid_eduroam_list = []
    signal_list = []
    magnetic_list = []
    rtt_data_100 = []
    
    path_anly_ip = []
    path_anly_as = []
                                 
    #Data from Server folder
    path = thedir+'/'+ 'server'
    for root, ser_dirs, files in os.walk(path):                                                                                      
        #if root_dirs in 'server':
            #print 'all_rtt_data: ', all_rtt_data
            #path = thedir+'/'+ root_dirs               
            #for root, ser_dirs, files in os.walk(path):                                                           
    
            ser_dirs.sort(reverse=True)  
                                                               
            if len(ser_dirs) >= 3:                  
                srv_dirs_arrange=ser_dirs[0:3]                                                            
            else:    
                srv_dirs_arrange=ser_dirs[0:len(ser_dirs)]                                                    
                            
            #srv_dirs_arrange = ser_dirs[6:9]
            
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
                        #added by derek
                        elif data["traceroute"] is None:
                            continue
                        elif data["traceroute"][0]["hops"] is None:
                            continue
                        
                        srv_traceroute_as = []
                        srv_traceroute_ip = []
                        srv_traceroute = data["traceroute"][0]["hops"]
                        
                        for x in reversed(srv_traceroute):
                            if x["AS"][0] is None:
                                continue
                            if "AS" + x["AS"][0] not in srv_traceroute_as:  srv_traceroute_as.append("AS" + x["AS"][0])
                            srv_traceroute_ip.append(x["ip"][0])
                        ####
                        
                        srv_latency_data = data["latency"][0]["rtt_ms"] 
                        timestamp_data=data["timestamp"]
                        srv_ip_data = data["latency"][0]["target_ip"]
                        tup = [srv_latency_data,
                               timestamp_data,
                               datetime.datetime.fromtimestamp(timestamp_data).strftime('%d %H:%M'), 
                               numpy.average(srv_latency_data),
                               srv_ip_data, 
                               #added by derek
                               srv_traceroute_as, 
                               srv_traceroute_ip
                               ####
                               ]
                               
                                
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
                            #m = 1
                            print 'OK'                    
                            if (sorted_srv_rtt_data[i][1] - all_rtt_data[m][aa][1] < 10) & (sorted_srv_rtt_data [i][4] == all_rtt_data[m][aa][4]):              
                                                    
                                rtt_list.append( sorted_srv_rtt_data[i][0] )
                                avgs.append( sorted_srv_rtt_data[i][3] )
                                label.append( sorted_srv_rtt_data[i][2] )
                                #print 'aplabel',label
                                cl_rtt_data.append(all_rtt_data[m][aa][3])
                                
                                #added by derek
                                #print "I am server:", sorted_srv_rtt_data[i][6]
                                #print "I am client:", all_rtt_data[m][aa][12]
                                #print 'data',sorted_srv_rtt_data[i][1] - all_rtt_data[m][aa][1],'-',sorted_srv_rtt_data [i][4],'-',all_rtt_data[m][aa][4]
                                path_anly_as.append( LevenshteinDistance(sorted_srv_rtt_data[i][5], all_rtt_data[m][aa][11]) )
                                if all_rtt_data[m][aa][12][0] is not None:
                                    path_anly_ip.append( LevenshteinDistance_for_ip(sorted_srv_rtt_data[i][6], all_rtt_data[m][aa][12]) )
                                #### 
                            aa+=1    
                        else:
                            break
                        
                                                    
            m=m+1    
    #end4 = timeit.timeit()
    #print "TIME4 =" , (end4-end3);
    
    # pearson coefficient  
    cl_rtt_data_value,e = pearsonr(avgs, cl_rtt_data)
    print 'label',label
    if len(label) != 0:                        
        ax3 = fig.add_subplot(k,1,3)
        ax4 = fig.add_subplot(k,1,3)
        #ax3.set_title( ' 3 days server response clinet latency data time series plot' )
        ax3.set_xlabel('Hour')
        ax3.set_ylabel('rtt_ms')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        plt.text(25, 1200, '3 days server response clinet latency data time series plot' , fontsize=14, ha='left', va='top')
        if ( cl_rtt_data_value >= 0 or cl_rtt_data_value < 0): 
            axt3 = 'pearson coefficient = ',cl_rtt_data_value
            ax3.annotate(axt3, xy=(1, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
                         ha='right', va='bottom')
        ax3, = plt.plot(avgs, label = 'match')
        ax4, = plt.plot(cl_rtt_data, label = 'client')
        l1 = plt.legend([ax3], ["server"], loc=1)
        l2 = plt.legend([ax4], ["client"], loc=2) 
        plt.gca().add_artist(l1) 
        plt.gca().add_artist(l2)
   
        ax13 = fig.add_subplot(k,1,15)
        #ax13.set_title( '3 days server response clinet path tracing (AS) Levenshtein Distance' )
        ax13.set_xlabel('Hour')
        ax13.set_ylabel('unit')
        
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        ax13.annotate('3 days server response clinet path tracing (AS) Levenshtein Distance' , xy=(0, 5), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',
                 ha='center', va='top')
        ax13, = plt.plot(path_anly_as, 'ko-')
        
        ax14 = fig.add_subplot(k,1,16)
        #ax14.set_title( '3 days server response clinet path tracing (IP) Levenshtein Distance' )
        ax14.set_xlabel('Hour')
        ax14.set_ylabel('unit')
        pylab.xticks(range(0,len(label)),label, rotation='vertical')
        plt.text(100, 2, '3 days server response clinet path tracing (IP) Levenshtein Distance' , fontsize=14, ha='left', va='top')
        ax14, = plt.plot(path_anly_ip,'ko-')
        
    
    rtt_list=[]
    avgs=[]
    label=[]
    cl_rtt_data=[]
    path_anly_ip=[]
    path_anly_as = []
        
    
               
    plt.show()

if __name__ == '__main__':
    main()
    pass