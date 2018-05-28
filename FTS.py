'''
Created on May 11, 2018

@author: rcpsi
'''

import numpy as np
import iFTS.Partioner as partitioner
import iFTS.TriangularFuzzySets as tfs

class FTS(object):
    '''
    classdocs
    '''

    def __init__(self, data, lb = None, ub = None, partition_method = 'triangular uniform', ftype = 'max'):
        '''
        Constructor
        '''
        #self.fuzzy_sets = fuzzy_sets 
        self.rules = None
        self.ftype = ftype
        self.data = data
        self.def_vals = [];
        
        # Define universe of discourse
        if not lb:
            lb = np.min(data)
        if not ub:
            ub = np.max(data)
        
        if partition_method == 'triangular uniform':
            self.partitions = partitioner.generate_uniform_triangular_partitions(lb, ub, 7)
            self.fuzzy_sets = tfs.TriangularFuzzySets(self.partitions)
            
    
    def __getattr__(self, attr):
        
        if attr == 'fuzzy_sets': # Get the list of fuzzy set parameters
            return self.fuzzy_sets
        elif attr == 'rules':
            return self.rules
        elif attr == 'def_vals':
            return self.def_vals
        else:
            raise AttributeError(attr) 
    
    def fuzzify(self, x, ftype = 'max', membership_matrix = None):
        """Fuzzify a value.

        Fuzzify a value in accordance with current partitions / fuzzy sets

        Args:
            x: Value or array of values to be fuzzified  

        Returns:
            y: Fuzzified value or array of values
            
        """
        
        if membership_matrix is None:
            membership_matrix = self.fuzzy_sets.compute_memberships(x)
        
        if ftype == 'max':
            return np.argmax(membership_matrix, 1)
            # I am assuming that any given x will be a member of at least one of the fuzzy sets 
            # TODO: Figure out what to do in case the assumption is not true
        else:
            return None
    
    def generate_rules(self):
        
        fuzzified_data = self.fuzzify(self.data,self.ftype)
        self.rules = []
                
        # Start using sets because it is neater
        for i in range(len(self.fuzzy_sets.centers)):
            self.rules.append(set())
        
        for i in range(len(fuzzified_data)-1):
            fuzzified_data[i]
            self.rules[fuzzified_data[i]].update(set([fuzzified_data[i+1]]))
        
        # Convert back to lists 
        for i in range(len(self.rules)):
            self.rules[i] = list(self.rules[i])
            
    def print_rules(self):
        
        # Check if the rule have already been generated
        if self.rules is None: # If not, generate them! 
            print('Generating rules ...')
            self.generate_rules(self.data, self.ftype)
        
        for i in range(len(self.rules)):
            if self.rules[i]: 
                s = 'A{}'.format(i+1) + '->'
                for j in range(len(self.rules[i])):
                    s = s + 'A{} '.format(self.rules[i][j]+1)     
                print(s)   
    
    def predict(self, x, dtype = 'center average'):
        
        if dtype == 'center average':
            return self.defuzzify_center_average(x)
        elif dtype == 'weighted average':
            return self.defuzzify_weighted_average(x)
        elif dtype == 'persistence':
            return self.persistence(x)
            
    def persistence(self, x):
        self.def_vals = x
        return x
    
    def defuzzify_weighted_average(self,x):
        """Computes the defuzzified (numerical) values of x according to the model defined by this fts .

        Args:
            x: Value or array of values 

        Returns:
            y: membership matrix
            
        """
        # Fuzzify
        membership_matrix = self.fuzzy_sets.compute_memberships(x)
        centers = self.fuzzy_sets.centers;
        
        def_vals = np.zeros(len(x)) #storage for the defuzified values
        # Find matching antecendents
        for i in range(len(x)):
            
            memberships = membership_matrix[i,:]                        
        
            # Defuzzify
            #For each rule
            for j in range(len(self.rules)):
                # Compute the membership of x in the antecendent j
                mu = memberships[j]
                term = 0;
                 
                if self.rules[j]:
                    for k in range(len(self.rules[j])):
                        term = term + centers[self.rules[j][k]]
                    
                    def_vals[i] = def_vals[i] + (term/len(self.rules[j]))*mu
                else: # If the rule is empty, adopt persistence
                    #print('[{}] : {}'.format(j,mu))
                    def_vals[i] = def_vals[i] + centers[j]*mu
              
        # Return defuzified values
        self.def_vals = def_vals
        return def_vals 
    
    def defuzzify_center_average(self,x):
        """Computes the defuzzified (numerical) values of x according to the model defined by this fts .

        Args:
            x: Value or array of values 

        Returns:
            y: membership matrix
            
        """
        # Fuzzify
        membership_matrix = self.fuzzy_sets.compute_memberships(x)
        print(np.sum(membership_matrix,1))
        centers = self.fuzzy_sets.centers;
        fuzzified_data = self.fuzzify(x,self.ftype,membership_matrix = membership_matrix)
        
        def_vals = np.zeros(len(fuzzified_data)) #storage for the defuzified values
        # Find matching antecendents
        for i in range(len(fuzzified_data)):
            # Find matching antecendents
            idx = fuzzified_data[i]
            
            matching_rule = self.rules[idx]
                        
            # If the data point has no pertinence with respect to any rule use the rule with the closest center to the data point\
            if not matching_rule:
                dists = (centers-x[i])**2
                closest = np.argmin(dists);
                def_vals[i] = centers[closest]
            else:    
                # Compute the degree of fulfilment (df) of the rule
                df = membership_matrix[i,fuzzified_data[i]]
            
                # Defuzzify
            
                for j in range(len(matching_rule)):
                    def_vals[i] = def_vals[i] + centers[matching_rule[j]] * df
        
                def_vals[i] = def_vals[i] / (df * len(matching_rule))    

        # Return defuzified values
        self.def_vals = def_vals
        return def_vals     
        
    