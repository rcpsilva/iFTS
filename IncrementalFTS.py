'''
Created on May 21, 2018

@author: rcpsi
'''

import numpy as np
import iFTS.Partioner as partitioner
import iFTS.TriangularFuzzySets as tfs
from iFTS.DataStats import DataStats
import matplotlib.pyplot as plt
import time

class IncrementalFTS(object):
    '''
    classdocs
    '''
    
    def __init__(self, data, lb = None, ub = None, partition_method = 'triangular uniform', ftype = 'max', dtype = 'center average', incremental = False):
        '''
        Constructor
        '''
        self.nsets = 7
        
        self.rules = None
        self.partitioner = None
        self.fuzzy_sets = None
        
        self.ftype = ftype
        self.dtype = dtype
        
        self.data = data
        self.ulb = None
        self.uub = None
        self.partitions = None
        self.fuzzy_sets = None
        self.current = data[len(data)-1]
        self.nsigmas = 3;
        
        # Stores basic data stats
        self.datastats = DataStats(np.mean(data), np.std(data), np.min(data), np.max(data),n = len(data))
        
        ''''
        # Define universe of discourse
        if not lb:
            self.ulb = np.minimum(self.datastats.min,self.datastats.mean - self.nsigmas*self.datastats.std)
        else:
            self.ulb = lb
        
        if not ub:   
            self.uub = np.maximum(self.datastats.max,self.datastats.mean + self.nsigmas*self.datastats.std)
        else:
            self.uub = ub
        '''
        
        if not lb:
            self.ulb =  self.datastats.min
        else:
            self.ulb = lb
            
        if not ub:
            self.uub =  self.datastats.max
        else:
            self.uub = ub
        
            
        # Generate initial partions    
        if partition_method == 'triangular uniform':
            self.partitioner = partitioner.generate_uniform_triangular_partitions
            self.partitions = self.partitioner(self.ulb, self.uub, self.nsets)
            self.fuzzy_sets = tfs.TriangularFuzzySets(self.partitions)
        elif partition_method == 'triangular uniform1':
            self.partitioner = partitioner.generate_uniform_triangular_partitions1
            self.partitions = self.partitioner(self.ulb, self.uub, self.nsets)
            self.fuzzy_sets = tfs.TriangularFuzzySets(self.partitions)
        
    def __getattr__(self, attr):
        
        if attr == 'fuzzy_sets':
            return self.fuzzy_sets
        elif attr == 'rules':
            return self.rules
        elif attr == 'datastats':
            return self.datastats
        elif attr == 'partitions':
            return self.partitions
        elif attr == 'ulb':
            return self.ulb
        elif attr == 'uub':
            return self.uub
        else:
            raise AttributeError(attr) 
        
    def run(self,x,idx,vals,p):
        
        # Update universe of discourse
        #print('## Update mean and std')
        n = self.datastats.n + 1 
        newmean = self.datastats.mean + (x - self.datastats.mean)/n
        var = self.datastats.std**2
        newstd =  np.sqrt( (n-2)/(n-1) * var + (1/n) * (x - self.datastats.mean)**2)
        
        
        self.datastats.mean = newmean;
        self.datastats.std = newstd;       
        ## Update max
        self.datastats.max = np.maximum(self.datastats.max,x)
        ## Update mean
        self.datastats.min = np.minimum(self.datastats.min,x)
        
        
        self.datastats.n += 1
        #print('# Updated stats \n {} | {} | {} | {} \n ----------------'.format(self.datastats.min,self.datastats.mean,self.datastats.max,self.datastats.std))
        
        
        #print('#Update universe of discourse')
        self.ulb = np.minimum(self.datastats.min,self.datastats.mean - self.nsigmas*self.datastats.std)
        self.uub = np.maximum(self.datastats.max,self.datastats.mean + self.nsigmas*self.datastats.std)
        
        #self.ulb = self.datastats.mean - self.nsigmas*self.datastats.std
        #self.uub = self.datastats.mean + self.nsigmas*self.datastats.std
        
        #self.ulb = np.minimum(self.datastats.min,x)
        #self.uub = np.maximum(self.datastats.max,x)
        
        
        #print('# Generate partitions and fuzzy sets')
        new_partitions = self.partitioner(self.ulb, self.uub, self.nsets)
        new_fuzzy_sets = tfs.TriangularFuzzySets(self.partitions)
        
        ## Fuzzify old centers according to the new fuzzy sets
        centers_membership_matrix = new_fuzzy_sets.compute_memberships(self.fuzzy_sets.centers)
        mappings = self.fuzzify(self.fuzzy_sets.centers, membership_matrix = centers_membership_matrix)
        
        self.partitions = new_partitions
        self.fuzzy_sets = new_fuzzy_sets
        
        #print('# Update rules')
        if not self.rules: # If there are no rules
            self.generate_rules()
            # Transforming rules into sets
            for i in range(self.nsets):
                self.rules[i] = set(self.rules[i])
        else: #if there are rules
            ## Check if there are updates to be made
            #if not ((mappings == np.arange(0,self.nsets)).all()): #Update rules
                ########## Improve this for efficiency! ################
                new_rules = self.rules.copy()
                for i in range(self.nsets):
                    for j in range(len(new_rules[i])):
                        new_rules[i][j] = mappings[new_rules[i][j]] 
            
                #self.rules = [set(r) for r in new_rules]
                
                for i in range(self.nsets):
                    self.rules[i] = set() # Eliminates copies if different fuzzy sets are mapped onto a single set
            
                for i in range(self.nsets):
                    self.rules[mappings[i]].update(set(new_rules[i]))  # Eliminates copies if different fuzzy sets mapped onto a single set
                
                ########################################################
            #else: # Transforming rules into sets
            #    for i in range(self.nsets):
            #        self.rules[i] = set(self.rules[i])
                
            
        ## Update rules with the new point
        antecendent = self.fuzzify([self.current])
        consequent = self.fuzzify([x])
                       
        self.rules[antecendent[0]].update(consequent)
            
            ## Update current state
            ### Convert back to lists 
        for i in range(len(self.rules)):
            self.rules[i] = list(self.rules[i])
        
        self.print_rules()
        
        self.current = x
        ##########################         
            
        # Make forecast
        p.append(self.predict([x]))
        return p
    
    def fuzzify(self, x, membership_matrix = None):
        """Fuzzify a value.

        Fuzzify a value in accordance with current partitions / fuzzy sets

        Args:
            x: Value or array of values to be fuzzified  

        Returns:
            y: Fuzzified value or array of values
            
        """
        
        if membership_matrix is None:
            membership_matrix = self.fuzzy_sets.compute_memberships(x)
        
        if self.ftype == 'max':
            return np.argmax(membership_matrix, 1)
            # I am assuming that any given x will be a member of at least one of the fuzzy sets 
            # TODO: Figure out what to do in case the assumption is not true
        else:
            return None
    
    def generate_rules(self):
        
        fuzzified_data = self.fuzzify(x = self.data)
        self.rules = []
                
        # Start using sets because it is neater
        for i in range(len(self.fuzzy_sets.centers)):
            self.rules.append(set())
        
        for i in range(len(fuzzified_data)-1):
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
    
    def predict(self, x):
        
        if self.dtype == 'center average':
            return self.defuzzify_center_average(x)
        elif self.dtype == 'weighted average':
            return self.defuzzify_weighted_average(x)
        elif self.dtype == 'persistence':
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
        if not self.rules: # If there are no rules
            self.generate_rules()
        
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
        fuzzified_data = self.fuzzify(x,membership_matrix = membership_matrix)
        
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
        
    