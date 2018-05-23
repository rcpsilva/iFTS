'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np
import matplotlib.pyplot as plt
import time
from iFTS.TriangularFuzzySets import TriangularFuzzySets
from iFTS.FTS import FTS
from iFTS.IncrementalFTS import IncrementalFTS
import iFTS.Partioner as pt
from pyFTS.data import TAIEX
import time


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
    #line, = axes.plot(xdata, ydata, 'r-')
    
   
    for i in range(nsamples):
        xdata.append(data[i,0])
        ydata.append(data[i,1])
        #print((data[i,0],data[i,1]))
        #line.set_xdata(xdata)
        #line.set_ydata(ydata)
        plt.plot(data[i,0],data[i,1],'r.')
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.000000001)
       

    plt.show()

def main():

    vals = TAIEX.get_data()
    #vals = generate_data(1000)
    #vals = vals[:,1];
    
    print(vals.shape)
    
    train_end = 2
        
    fts = IncrementalFTS(data = vals[0:train_end], dtype = 'center average', incremental = True)
    # Train FTS
    #fts.generate_rules()
    #fts.print_rules()
    
    for i in range(2500):
        fts.run(vals[train_end+i],i,vals)
        
    
    #fts.fuzzy_sets.plot_fuzzy_sets(np.min(vals), np.max(vals),begin = -500 , scale = 400, nsteps = 1000)
    
    #p3 = fts.predict(vals[train_end:(len(vals)-1)])
    #p2 = fts.predict(vals[train_end:(len(vals)-1)], dtype = 'center average')
    #p1 = fts.predict(vals[train_end:(len(vals)-1)], dtype = 'persistence')
    
    #plt.plot(p3)
    #plt.plot(vals[(train_end):(len(vals))])
    #plt.plot(np.linspace(train_end, len(vals), len(p3)),p2)
    #plt.plot(np.linspace(train_end+1, len(vals), len(p3)),p1)
    #plt.plot(np.linspace(train_end+1, len(vals), len(p3)),vals[(train_end+1):(len(vals))])
    
    plt.show()
    
if __name__ == '__main__':
    main()
    
    