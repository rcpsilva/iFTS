'''
Created on May 11, 2018

@author: rcpsi
'''

class FTS(object):
    '''
    classdocs
    '''


    def __init__(self, set_parameters):
        '''
        Constructor
        '''
        self.set_parameters = set_parameters 
        self.rules = []
    
    
    
    def fuzzify(self, x):
        """Fuzzify a value.

        Fuzzify a value in accordance with current partitions / fuzzy sets

        Args:
            x: Value or array of values to be fuzzified  

        Returns:
            y: Fuzzified value or array of values
            
        """
    
        
    def defuzzify(self, x):
        """Computes the defuzzified (numerical) values of x according to the model defined by this fts .

        Args:
            x: Value or array of values 

        Returns:
            y: membership matrix
            
        """

    def update_partitions(self,partitions):
        
        self.partitions = partitions
        
        
    