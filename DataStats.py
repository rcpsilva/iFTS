'''
Created on May 21, 2018

@author: rcpsi
'''

class DataStats(object):
    '''
    classdocs
    '''


    def __init__(self, mean, std, dmin, dmax, n):
       
        self.mean = mean
        self.std = std
        self.max = dmax
        self.min = dmin
        self.n = n
        
        
    def __setattr__(self, attr, value):
        if attr == 'mean': # Set the list of fuzzy set parameters
            self.__dict__[attr] = value
        elif attr == 'std': 
            self.__dict__[attr] = value
        elif attr == 'max': 
            self.__dict__[attr] = value
        elif attr == 'min': 
            self.__dict__[attr] = value
        elif attr == 'n': 
            self.__dict__[attr] = value
        else:
            raise AttributeError(attr)
    
    def __getattr__(self, attr):
        if attr == 'mean': # Get the list of fuzzy set parameters
            return self.parameters
        elif attr == 'std': # Get the list of fuzzy set parameters
            return self.parameters
        elif attr == 'max': # Get the list of fuzzy set parameters
            return self.parameters
        elif attr == 'min': # Get the list of fuzzy set parameters
            return self.parameters
        elif attr == 'n': # Get the list of fuzzy set parameters
            return self.parameters
        else:
            raise AttributeError(attr) 
        