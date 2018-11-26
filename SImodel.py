#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:13:14 2018

@author: lequang
"""
from __future__ import division

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt



def infection_model(network, p, flights, start_node):

    #Extract data of first flight and last flight 
    

    #Create dataframe storing airport and infection time 
    airports = sorted(network.nodes())
    inf_time = np.full((len(airports),), np.inf)
    infection = pd.DataFrame({"Airport":airports, "InfectionTime": inf_time}) 
    
    #Set the infection time of first infected node:
    infection.InfectionTime[start_node] = flights.StartTime.min()
    #Loop over flights and start infection 
    for i in range(len(flights)):
        source = flights.Source[i]
        source_inf_time = infection.InfectionTime[source]
        if (source_inf_time < flights.StartTime[i]):
            random = np.random.rand()
            if random <= p:
                target = flights.Destination[i]
                target_cur_inf_time = infection.InfectionTime[target]
                target_new_inf_time = flights.EndTime[i]
                if target_new_inf_time < target_cur_inf_time:
                    infection.InfectionTime[target] = target_new_inf_time
    return infection


flights = pd.read_csv("./events_US_air_traffic_GMT.txt", sep = " ")

#Read in network data
networkpath = "./aggregated_US_air_traffic_network_undir.edg"
network = nx.read_weighted_edgelist(networkpath, nodetype = int )

#Run model with p = 1
start_node_0 = flights.Source[0] #Initiate the first infected node
flights = flights.sort_values("StartTime")
start_time = flights.StartTime.min() #First infected time
end_time = flights.EndTime.max()

infection = infection_model(network, 0.05 ,flights, start_node_0)
infection_times = infection.InfectionTime

print("Anchorage infection time: ",infection.InfectionTime[41])

#Task 2: Effect of probability p on spreading speed

#Task 2
def averaged_prevalence_visualization(infection, start, end, p, label):
    stepsize = 50    
    t = np.linspace(start, end, stepsize)  #To increase this stepsize
    p_t = np.zeros((stepsize,10), dtype=float)
    for k in range(0,10):
        for j in range (0,stepsize):
            count = (infection.InfectionTime < t[j]).sum()
            prob = float(count/len(infection))
            p_t[j,k] = prob
    prevalence = np.average(p_t, axis = 1)
    plt.plot(t, prevalence, label = label)

fig = plt.figure(figsize=(10,7))
for p in (0.01, 0.05, 0.1, 0.5, 1): 
    infection_p = infection_model(network, p,flights, start_node_0)
    averaged_prevalence_visualization(infection_p, start_time, end_time, p, p)
plt.xlabel("Time")
plt.ylabel("Averaged prevalence")
plt.legend()
plt.show()

