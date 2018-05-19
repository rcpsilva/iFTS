'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np
import matplotlib.pyplot as plt
import time
from TriangularFuzzySets import TriangularFuzzySets
from FTS import FTS
import Partioner as pt
from pyFTS.data import TAIEX


def generate_data(nsamples):

    timeStamps = np.linspace(10, 1000, num=nsamples)*0.05+50;
    irradiance = np.sin(timeStamps/np.pi)*np.sin(timeStamps)*timeStamps*3 + 200

    data = np.concatenate((np.transpose([timeStamps]),np.transpose([irradiance])), axis = 1)

    return data

def plot_data(data):
    
    xdata = []
    ydata = []
 
    plt.show()
 
    nsamples = data.shape[0]
 
    axes = plt.gca()
    axes.set_xlim(np.min(data[:,0]), np.max(data[:,0]), nsamples)
    axes.set_ylim(np.min(data[:,1]), np.max(data[:,1]))
    line, = axes.plot(xdata, ydata, 'r-')
    
   
    for i in range(nsamples):
        xdata.append(data[i,0])
        ydata.append(data[i,1])
        print((data[i,0],data[i,1]))
        line.set_xdata(xdata)
        line.set_ydata(ydata)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.001)
       

    plt.show()

def main():
    ''''
    # Load data
    nsamples = 500
    vals = generate_data(nsamples)
    #plot_data(data)
    
    # Set up FTS parameter
    
    # Generate partitioner
    set_parameters = pt.generate_uniform_triangular_partitions(np.min(vals[:,1]), np.max(vals[:,1]), 6, 50)
    # Generate fuzzysets
    fuzzysets = TriangularFuzzySets(set_parameters)
    fuzzysets.plot_fuzzy_sets(100, 320,30 , 10, 1000)
    
    train_end = 250
    plt.plot(vals[:,0],vals[:,1])
    plt.plot(vals[0:train_end,0],vals[0:train_end,1])
    
    
    # Generate FTS
    fts = FTS(fuzzysets,data = vals[0:train_end,1])
    # Train FTS
    fts.generate_rules()
    
    fts.print_rules()
    
    p1 = fts.predict(vals[train_end:499,1], dtype = 'weighted average')
    p2 = fts.predict(vals[train_end:499,1], dtype = 'center average')
    p3 = fts.predict(vals[train_end:499,1], dtype = 'center')
    
    plt.subplot(2, 1, 1)
    fuzzysets.plot_fuzzy_sets(100, 320,30 , 10, 1000)
    plt.plot(vals[:,0],vals[:,1])
    #plt.plot(vals[(train_end+1):500,0],p1)
    #plt.plot(vals[(train_end+1):500,0],p2)
    plt.plot(vals[(train_end+1):500,0],p3)
    
    plt.subplot(2, 1, 2)
    plt.hist(vals[:,1], bins='auto')

    plt.show()
    #print(p)
    '''
    #vals = TAIEX.get_data()
    vals = generate_data(4000)
    vals = vals[:,1];
    
    print(vals.shape)
    plt.plot(vals)
    
    # Generate partitioner
    set_parameters = pt.generate_uniform_triangular_partitions(np.min(vals), np.max(vals), 7)
    # Generate fuzzysets
    fuzzysets = TriangularFuzzySets(set_parameters)
    fuzzysets.plot_fuzzy_sets(np.min(vals), np.max(vals),begin = -500 , scale = 400, nsteps = 1000)
    
    train_end = 250
    
    fts = FTS(fuzzysets,data = vals[0:train_end])
    # Train FTS
    fts.generate_rules()
    fts.print_rules()
    
    p3 = fts.predict(vals[train_end:(len(vals)-1)], dtype = 'defuzz1')
    p2 = fts.predict(vals[train_end:(len(vals)-1)], dtype = 'center average')
    p1 = fts.predict(vals[train_end:(len(vals)-1)], dtype = 'persistence')
    
    plt.plot(np.linspace(train_end+1, len(vals), len(p3)),p3)
    #plt.plot(np.linspace(train_end, len(vals), len(p3)),p2)
    #plt.plot(np.linspace(train_end+1, len(vals), len(p3)),p1)
    #plt.plot(np.linspace(train_end+1, len(vals), len(p3)),vals[(train_end+1):(len(vals))])
    
    print(p3.shape)
    print(vals[(train_end+1):(len(vals))].shape)
    
    
    plt.show()
    
if __name__ == '__main__':
    main()
    
    