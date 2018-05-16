'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np

    
def generate_uniform_triangular_partitions(lb, ub, num, width):
    
    centers = np.linspace(lb, ub, num)
    partitions = []
    for c in centers:
        partitions.append([c-width/2,c,c+width/2])
         
    return partitions