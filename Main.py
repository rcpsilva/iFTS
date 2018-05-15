'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np
import matplotlib.pyplot as plt
import time
from iFTS.TriangularFuzzySets import TriangularFuzzySets


def generate_data(nsamples):

    timeStamps = np.linspace(10, 1000, num=nsamples)*0.05+50;
    irradiance = np.sin(timeStamps)*timeStamps+timeStamps*5

    data = np.concatenate((np.transpose([timeStamps]),np.transpose([irradiance])), axis = 1)

    return data

def plot_data(data):
    
    xdata = []
    ydata = []
 
    plt.show()
 
    nsamples = data.shape[0]
 
    axes = plt.gca()
    axes.set_xlim(50, nsamples)
    axes.set_ylim(100, 1000)
    line, = axes.plot(xdata, ydata, 'r-')
    
   
    for i in range(nsamples):
        xdata.append(data[i,0])
        ydata.append(data[i,1])
        print((data[i,0],data[i,1]))
        line.set_xdata(xdata)
        line.set_ydata(ydata)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.1)
       

    plt.show()

def main():
    set_parameters = [[0.3,1,1.7],[1.3,2,2.7],[2.3,3,3.7],[3.3,4,4.7],[4.3,5,5.7]]
    fuzzysets = TriangularFuzzySets(set_parameters)
    fuzzysets.plot_fuzzy_sets(0, 6, 1000)
    

if __name__ == '__main__':
    main()
    
    