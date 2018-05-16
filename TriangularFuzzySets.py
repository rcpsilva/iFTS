'''
Created on May 15, 2018

@author: rcpsi
'''
from iFTS.FuzzySets import FuzzySets

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
        
        if x < a or x > c:
            return 0
        elif x >= a and x <= b:
            return (x-a)/(b-a)
        elif x == b:
            return 1
        elif x>b and x<=c:
            return (c-x)/(c-b)
        
        return None