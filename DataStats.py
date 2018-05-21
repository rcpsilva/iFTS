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