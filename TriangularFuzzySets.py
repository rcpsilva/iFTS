'''
Created on May 15, 2018

@author: rcpsi
'''
from iFTS.FuzzySets import FuzzySets
import numpy as np

class TriangularFuzzySets(FuzzySets):
    '''
    classdocs
    '''
    
    def __init__(self, parameters = []):
        '''
        Constructor
        '''
        # Call superclass (FuzzySets) constructor
        super(TriangularFuzzySets, self).__init__(parameters)


    def centers(self):
        centers = np.zeros(len(self.parameters))
        for i in range(len(self.parameters)):
            centers[i] = self.parameters[i][1]
        
        return centers
        
    def membership(self,x,setparams):
        """Computes the membership of a value with respect to the fuzzy set defined by setparameters. 
        This specific method implements triangular fuzzy sets. 

        Args:
            x: Point
            setparams: Fuzzy set paramenters

        Returns:
            mu: membership 
            
        """
    
            # For readability
        a = setparams[0];
        b = setparams[1];
        c = setparams[2];
        
        #print('Partitioner: {} {} {}'.format(a,b,c))
        
        if np.isinf(-a) and x < b:
            return 1
        if np.isinf(c) and x > b:
            return 1
        
        if x < a or x > c:
            return 0
        elif x >= a and x <= b:
            return (x-a)/(b-a)
        elif x == b:
            return 1
        elif x>b and x<=c:
            return (c-x)/(c-b)
        
        return None