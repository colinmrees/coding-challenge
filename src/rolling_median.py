#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:37:07 2018

@author: Colin M Rees
"""

import pandas as pd
#import numpy as np
import sys
import time
import datetime
#import matplotlib.pyplot as plt
#import scipy.stats as sta

#networkx library more performant for a dynamic graph than iGraph
import networkx as nx
import getopt

#import queue  #may want to use a queue for multithreaded solution


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

def main( argv ):
    
    G = nx.Graph()
    
    history = []#may ues queue instead
    median = 0
    benchmark = False
    
    windowSize = datetime.timedelta(seconds=60)
    
    infilename = 'venmo_input/venmo-trans.txt'
    outfilename = 'venmo_output/output.txt'
    try:
        opts, args = getopt.getopt(argv,"hi:o:b")
    except getopt.GetoptError:
        print( 'rolling_median.py -i <inputfilepath> -o <outputfilepath>' )
        sys.exit(0)
    for opt, arg in opts:
        if ( opt == '-h' ):
            print( 'rolling_median.py -i <inputfilepath> -o <outputfilepath>' )
            sys.exit(0)
        elif ( opt == '-i' ):
            infilename = arg
        elif ( opt == '-o' ):
            outfilename = arg
        elif ( opt == '-b' ):
            benchmark = True
            
    if ( benchmark ):
        startTime = time.process_time()
    
    outfile=open(outfilename, 'w+') # 'a+' instead to append to a file
    try:
        infile=open(infilename, 'r')
    except FileNotFoundError:
        outfile.write("No Valid Input File")
        exit(0)
    
    #Iterate through records in input file
    for x in infile.readlines():
        
        try:
            transaction = pd.read_json(x, typ='series')
        except ValueError:
            #Invalid Data - Invalid Syntax or Duplicate Field - Ignore and skip record
            continue
        
        #columns= ["actor", "target", "created_time"]
        try:
            t_data = (transaction["actor"], transaction["target"], datetime.datetime.strptime(transaction["created_time"], '%Y-%m-%dT%H:%M:%SZ') )
        except KeyError:
            #Invalid Data Format - Ignore and skip record
            continue
        except TypeError:
            #Invalid Data Format - Ignore and skip record
            continue
        except ValueError:
            #Invalid Data Format - Ignore and skip record
            continue
        
        newEdge = True
        if( len(history) > 0 and t_data[2] < history[len(history)-1][2] ):
            if( history[len(history)-1][2] - t_data[2] >= windowSize ):
                newEdge = False
            else:
                iter = len(history)-1
                while( t_data[2] < history[iter-1][2] and iter > 0 ):
                    iter -= 1;
                history.insert(iter, t_data)            
        else:
            history.append(t_data)
            while( t_data[2] - history[0][2] >= windowSize ):
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
    if( benchmark ):
        sys.stderr.write( "Runtime: " + str(time.process_time() - startTime) + "\n" )

if __name__ == "__main__":
    main(sys.argv[1:])