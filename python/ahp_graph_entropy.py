#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 11:38:37 2026

@author: nahamlet
"""

import os
from pathlib import Path

def set_project_root():
    # Start from the directory containing this notebook
    # (In Spyder/IPython, __file__ might not exist, so we fallback to os.getcwd())
    try:
        current_dir = Path(__file__).resolve().parent
    except NameError:
        current_dir = Path(os.getcwd()).resolve()

    # Traverse upward until we find the repository root marker
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / '.git').exists():
            os.chdir(parent)
            import sys
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            print(f"Working directory successfully set to repository root: {parent}")
            return parent
            
    print("Warning: .git root not found. Remaining in current directory.")
    return current_dir

# Execute the path adjustment
project_root = set_project_root()


#%%


class calculateHierarchyModelEntropy:
    def __init__(self,
                 comparative_judgements = None):
        
        self.comparative_judgements = comparative_judgements
    
    #
    def construct_reciprocal_matrix_from_comparative_judgements(self):
    
        from itertools import product
        from pandas import DataFrame, concat
        
        evidentiary_span = (set(ho_mc.comparative_judgements['reference_factor'])
                                 .union(self.comparative_judgements['comparative_factor']))
        
        pairwise_span = (DataFrame(data = product(evidentiary_span,
                                                  repeat = 2       ),
                                  columns = ['reference_factor',
                                             'comparative_factor'])   )
        
        
        reciprocal_matrix_off_diagonals = concat(objs = [pairwise_span
                                                           .merge(right = self.comparative_judgements),
                                                         pairwise_span
                                                           .merge(right = self.comparative_judgements
                                                                              .rename(columns = {'reference_factor' : 'comparative_factor',
                                                                                                 'comparative_factor' : 'reference_factor'})
                                                                              .assign(importance = lambda Ξ : Ξ['importance']
                                                                                                               .apply(func = lambda ξ : 1/ξ)))])
        
        reciprocal_matrix = (pairwise_span
                                    .merge(right = reciprocal_matrix_off_diagonals,
                                           how = 'left'                             )
                                    .fillna(value = 1)
                                    .pivot(index = 'reference_factor',
                                           columns = 'comparative_factor',
                                           values = 'importance'           )
                                    .reset_index(drop = False)                       )
        
        self.reciprocal_matrix = reciprocal_matrix
        
        return self.reciprocal_matrix
    #
    def calculate_priority_vector_from_reciprocal_matrix(self):
    
        from numpy import argmax, real, sum
        from numpy.linalg import eig
        
        (self.Λ,
         self.Χ) =  eig(ho_mc.reciprocal_matrix
                             .set_index(keys = 'reference_factor',
                                        drop = True                )
                             .to_numpy()                             )
        
        priority_vector_array = list(map(float,
                                         real(self.Χ[:, argmax(real(self.Λ))]/sum(self.Χ[:, argmax(real(self.Λ))]))))
        self.priority_vector = dict(zip(self.reciprocal_matrix
                                            ['reference_factor'],
                                        priority_vector_array))

        
        return self.priority_vector
    #
    def join_priority_vector_to_reciprocal_matrix(self):
        
        from pandas import Series
    
        self.reciprocal_matrix_priority_vector = (self.reciprocal_matrix
                                                        .merge(right = Series(data = self.priority_vector,
                                                                              name = 'priority_vector')
                                                                        .to_frame()
                                                                        .rename_axis(index = 'reference_factor')
                                                                        .reset_index(drop = False))             )
        
        return self.reciprocal_matrix_priority_vector
    #



#%%



#%%


from pandas import read_csv

path_to_judgement_comparison = './data/bu-et-al-pemfc-judgement-comparison.csv'

judgement_comparison = (read_csv(filepath_or_buffer = path_to_judgement_comparison)
                            .set_index(keys = 'hierarchy_model',
                                       drop = True              ))






#%%

ho_mc = calculateHierarchyModelEntropy(comparative_judgements = judgement_comparison.loc['objective_criterion']
                                                                                    .reset_index(drop = True)   )

ho_mc.construct_reciprocal_matrix_from_comparative_judgements()
ho_mc.calculate_priority_vector_from_reciprocal_matrix()
ho_mc.join_priority_vector_to_reciprocal_matrix()



#%%

from networkx import DiGraph

ho_mc.comparative_judgement_network = DiGraph()


ho_mc.comparative_judgement_network.add_edges_from(
                                                     ho_mc.comparative_judgements
                                                          .assign(importance = lambda Ξ : Ξ['importance']
                                                                                           .apply(func = lambda ξ : {'importance' : ξ}))
                                                          [['comparative_factor',
                                                            'reference_factor',
                                                            'importance'           ]]
                                                          .to_records(index = False)
                                                   ) 


#%%





#%%






#%%






#%%






#%%






#%%






#%%






#%%






#%%






#%%
