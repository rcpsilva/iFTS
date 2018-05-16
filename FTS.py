'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np

class FTS(object):
    '''
    classdocs
    '''


    def __init__(self, fuzzy_sets):
        '''
        Constructor
        '''
        self.fuzzy_sets = fuzzy_sets 
        self.rules = None
    
    def __getattr__(self, attr):
        
        if attr == 'fuzzy_sets': # Get the list of fuzzy set parameters
            return self.fuzzy_sets
        elif attr == 'rules':
            return self.rules
        else:
            raise AttributeError(attr) 
    
    
    
    def fuzzify(self, x, ftype = 'max'):
        """Fuzzify a value.

        Fuzzify a value in accordance with current partitions / fuzzy sets

        Args:
            x: Value or array of values to be fuzzified  

        Returns:
            y: Fuzzified value or array of values
            
        """
        
        membership_matrix = self.fuzzy_sets.compute_memberships(x)
        
        if ftype == 'max':
            return np.argmax(membership_matrix, 1)  \
            # I am assuming that any given x will be a member of at least one of the fuzzy sets 
            # TODO: Figure out what to do in case the assumption is not true
        else:
            return None
    
    def generate_rules(self, data, ftype = 'max'):
        
        fuzzified_data = self.fuzzify(data,ftype)
        self.rules = []
                
        # Start using sets because it is neater
        count = 0
        while count <= np.max(fuzzified_data):
            self.rules.append(set())
            count += 1
        
        for i in range(len(fuzzified_data)-1):
            fuzzified_data[i]
            self.rules[fuzzified_data[i]].update(set([fuzzified_data[i+1]]))
        
        # Convert back to lists 
        for i in range(len(self.rules)):
            self.rules[i] = list(self.rules[i])
            
        
    
    def print_rules(self):
        
        print(len(self.rules))
        
        for i in range(len(self.rules)):
            s = 'A{}'.format(i+1) + '->'
            for j in range(len(self.rules[i])):
                s = s + 'A{} '.format(self.rules[i][j]+1)     
            print(s)   
            
    
    def defuzzify(self, x):
        """Computes the defuzzified (numerical) values of x according to the model defined by this fts .

        Args:
            x: Value or array of values 

        Returns:
            y: membership matrix
            
        """

    def update_partitions(self,partitions):
        
        self.partitions = partitions
        
        
    