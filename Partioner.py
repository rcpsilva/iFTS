'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np

    
def generate_uniform_triangular_partitions(lb, ub, num):
    
    centers = np.linspace(lb, ub, num)
    width = abs(centers[0]-centers[1])
    partitions = []
    for c in centers:
        partitions.append([c-width,c,c+width])
         
    return partitions