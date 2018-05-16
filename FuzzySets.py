'''
Created on May 15, 2018

@author: rcpsi
'''

from abc import abstractmethod, ABCMeta
import numpy as np
import matplotlib.pyplot as plt
 
class FuzzySets(metaclass = ABCMeta):
    '''
    classdocs
    
    '''

    def __init__(self, parameters = []):
        '''
        Constructor
        '''
        self.parameters = parameters
    
    def __setattr__(self, attr, value):
        if attr == 'parameters': # Set the list of fuzzy set parameters
            self.__dict__[attr] = value
        else:
            raise AttributeError(attr)
        
    def __getattr__(self, attr):
        if attr == 'parameters': # Get the list of fuzzy set parameters
            return self.parameters
        else:
            raise AttributeError(attr) 
    
    def compute_memberships(self, x):
        """Computes the membership of a value or array of values with respect to 'this' fuzzysets.

        Args:
            x: Value or array of values 

        Returns:
            y: membership matrix
            
        """
        nvalues = len(x)
        nsets = len(self.parameters)
        membership_matrix = np.zeros([nvalues,nsets])
        
        for i in range(nvalues):
            for j in range(nsets):
                membership_matrix[i,j] = self.membership(x[i],self.parameters[j])
        
        return membership_matrix
        
    @abstractmethod    
    def membership(self,x,setparams):
        """Computes the membership of a value with respect to the fuzzy set defined by setparames.

        Args:
            x: Point
            setparams: Fuzzy set paramenters

        Returns:
            mu: membership 
            
        """
        pass
    
    @abstractmethod    
    def centers(self):
        """Computes the membership of a value with respect to the fuzzy set defined by setparames.

        Args:
            x: Point
            setparams: Fuzzy set paramenters

        Returns:
            mu: membership 
            
        """
        pass    
            
    def plot_fuzzy_sets(self, start, stop, nsteps = 1000):       
        """Plots the fuzzy sets for a given interval.

        Args:
            start: starting point
            stop: stopping point
            nsteps: number of steps
            
        """
        
        #generate array of points
        x = np.linspace(start,stop,nsteps)
        
        #Compute memberships
        membership = self.compute_memberships(x) 
    
        #Plot sets
        for i in range(membership.shape[1]):
            plt.plot(x,membership[:,i])
            
        plt.show()     
            