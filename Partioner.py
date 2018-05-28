'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np
from cmath import inf


def generate_uniform_triangular_partitions(lb, ub, num):
    
    # the membership is 1 below lb of above ub
    
    centers = np.linspace(lb, ub, num)
    width = abs(centers[0]-centers[1])
    partitions = []
    
    for c in centers:
        partitions.append([c-width,c,c+width])
    
    partitions[0][0] = -np.inf
    partitions[len(partitions)-1][2] = np.inf
         
    return partitions
    
def generate_uniform_triangular_partitions1(lb, ub, num):
    
    centers = np.linspace(lb, ub, num)
    width = abs(centers[0]-centers[1])
    partitions = []
    for c in centers:
        partitions.append([c-width,c,c+width])
                
    return partitions