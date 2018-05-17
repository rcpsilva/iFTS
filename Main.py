'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np
import matplotlib.pyplot as plt
import time
from iFTS.TriangularFuzzySets import TriangularFuzzySets
from iFTS.FTS import FTS
import iFTS.Partioner as pt


def generate_data(nsamples):

    timeStamps = np.linspace(10, 1000, num=nsamples)*0.05+50;
    irradiance = np.sin(timeStamps/np.pi)*np.sin(timeStamps)*timeStamps + 200

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
    
    p = fts.predict(vals[train_end:499,1])
    
    plt.subplot(2, 1, 1)
    fuzzysets.plot_fuzzy_sets(100, 320,30 , 10, 1000)
    plt.plot(vals[:,0],vals[:,1],vals[(train_end+1):500,0],p)
    plt.plot(vals[(train_end+1):500,0],p)
    
    plt.subplot(2, 1, 2)
    plt.hist(vals[:,1], bins='auto')

    plt.show()
    #print(p)
    

if __name__ == '__main__':
    main()
    
    