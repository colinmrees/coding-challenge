# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:37:07 2018

@author: Colin M Rees
"""

import pandas as pd
import numpy as np
import sys
import time
import datetime
import matplotlib.pyplot as plt
import scipy.stats as sta

#networkx library more performant for a dynamic graph than iGraph
import networkx as nx

#import queue  #may want to use a queue for multithreaded solution


columns= ["actor", "target", "created_time"]

G = nx.Graph()


def add_transaction( G, actor, target ):
    
    if( G.has_edge(actor, target) ):
        G[actor][target]['weight'] += 1
    else:
        G.add_edge( actor, target, weight=1  )


def remove_transaction( G, actor, target ):
    
    if( G[actor][target]['weight'] == 1 ):
        G.remove_edge(actor, target)
        if( len(G[actor]) == 0 ):
            G.remove_node(actor)
        if( len(G[target]) == 0 ):
            G.remove_node(target)
    else:
        G[actor][target]['weight'] -= 1


#nodeIDs = 0
nodes = {}
history = []#queue.Queue()
median = 0

windowSize = datetime.timedelta(seconds=60)

infilename = 'venmo_input/venmo-trans.txt'
infile=open(infilename, 'r')
outfilename = 'venmo_output/output.txt'
outfile=open(outfilename, 'w+')
for x in infile.readlines():
    transaction = pd.read_json(x, typ='series')
    
    t_data = (transaction["actor"], transaction["target"], datetime.datetime.strptime(transaction["created_time"], '%Y-%m-%dT%H:%M:%SZ') )
    
    newEdge = True
    if( len(history) > 0 and t_data[2] < history[len(history)-1][2] ):
        if( history[len(history)-1][2] - t_data[2] > windowSize ):
            newEdge = False
        else:
            iter = len(history)-1
            while( t_data[2] < history[iter-1][2] and iter > 0 ):
                iter -= 1;
            history.insert(iter, t_data)            
    else:
        history.append(t_data)
        while( t_data[2] - history[0][2] > windowSize ):
            removed = history.pop(0)
            remove_transaction( G, removed[0], removed[1] )
        
    if( newEdge ):
        add_transaction(G, t_data[0], t_data[1]) #add new transaction record
        
        #calculate median degree
        degreeList = sorted(dict(G.degree()).values())
        median = degreeList[len(G)//2]
        if ( len(G) % 2 == 0 ):
            median = (median + degreeList[len(G)//2 - 1 ] )/ 2
            
#        print( "Median Degree = " + str(median)  + " # of Transactions = " + str(G.size(weight='weight')) + " Time = " + str( t_data[2] ) )
#    else:
#        print( "New Transaction outside running time window. No Change. ( t = -" + str(history[len(history)-1][2] - t_data[2] ) + " )" )
#    nx.draw(G)
#    plt.show()
#    print( history )
    
    outfile.write( '{:.2f}\n'.format(median) )

infile.close()
outfile.close()