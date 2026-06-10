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
        self.hierarchy_model = list(set(self.comparative_judgements.index))[0]
        
        self.construct_hierarchy_model_tournament_graph()
    
    #
    def hash_tuple(self, 
                   tuple_to_hash, 
                   hash_length=24):
        """
        Serializes an iterable (tuple, list, or string) and returns its SHA-256 hash
        truncated to a specific length.
        """
        from hashlib import sha256
        
        # Coerce elements to strings and join them into a single string
        serialized = ''.join(map(str, tuple_to_hash))
        
        # Generate the SHA-256 hex digest and truncate to the desired length
        return sha256(serialized.encode('utf-8')).hexdigest()[:hash_length]
    #
    def construct_reciprocal_matrix_from_comparative_judgements(self):
    
        from itertools import product
        from pandas import DataFrame, concat
        
        evidentiary_span = (set(self.comparative_judgements['reference_factor'])
                                 .union(self.comparative_judgements['comparative_factor']))
        
        pairwise_span = (DataFrame(data = product(evidentiary_span,
                                                  repeat = 2       ),
                                  columns = ['reference_factor',
                                             'comparative_factor'])   )
        
        
        reciprocal_matrix_off_diagonals = concat(objs = [pairwise_span
                                                           .merge(right = self.comparative_judgements),
                                                         pairwise_span
                                                           .merge(right = self.comparative_judgements
                                                                              .rename(columns = {'reference_factor' : 'comparative_factor_ι',
                                                                                                 'comparative_factor' : 'reference_factor_ι'})
                                                                              .rename(columns = {'comparative_factor_ι' : 'comparative_factor',
                                                                                                 'reference_factor_ι' : 'reference_factor'})
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
         self.Χ) =  eig(self.reciprocal_matrix
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
    def calculate_geometric_mean_priority_vector(self):
    
        reciprocal_matrix_geometric_mean = (
                                             self.reciprocal_matrix
                                                  .set_index(keys = 'reference_factor',
                                                             drop = True                )
                                                  .product(axis = 1)
                                                  .map(func = lambda ψ : pow(ψ,
                                                                             1/self.reciprocal_matrix.shape[0]))
                                                  
                                             )
        
        self.geometric_mean_priority_vector = (
                                                 reciprocal_matrix_geometric_mean
                                                         .map(func = lambda φ : φ/reciprocal_matrix_geometric_mean.sum())
                                                         .to_dict()
                                               )
        
        return self.geometric_mean_priority_vector
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
    def construct_comparative_judgement_network(self):
    
        from networkx import DiGraph
        
        self.comparative_judgement_network = DiGraph()
        
        
        self.comparative_judgement_network.add_edges_from(
                                                          self.comparative_judgements
                                                              .assign(
                                                                      comparative_factor = lambda Η : Η['comparative_factor']
                                                                                                       .apply(func = lambda η : self.hierarchy_model
                                                                                                                                + ':'
                                                                                                                                + η                   ),
                                                                      reference_factor = lambda Χ : Χ['reference_factor']
                                                                                                     .apply(func = lambda χ :   self.hierarchy_model
                                                                                                                              + ':'
                                                                                                                              + χ                    ),
                                                                      importance = lambda Ξ : Ξ['importance']
                                                                                               .apply(func = lambda ξ : {'importance' : ξ})
                                                                      )
                                                              [['comparative_factor',
                                                                'reference_factor',
                                                                'importance'           ]]
                                                              .to_records(index = False)
                                                           )
        
        return self.comparative_judgement_network.edges()
    #
    def construct_comparative_judgement_network_plot(self):
    
        from numpy import sign
        from networkx import circular_layout, draw_networkx_nodes, draw_networkx_labels,draw_networkx_edges
        import matplotlib.pyplot as plt
        
        apply_coordinate_offset = lambda χ : (χ[0] - 0.1 * sign(χ[0]),
                                              χ[1] - 0.3 * sign(χ[1]))
        
        plt.rcParams['font.style'] = 'italic'
        
        vertex_positions  = circular_layout(G = self.comparative_judgement_network)
        
        (judgement_graph_figure,
         judgement_graph_axes   ) = plt.subplots(nrows = 1,
                                                 ncols = 1,
                                                 figsize = (5, 3.75))
        
        draw_networkx_nodes(G = self.comparative_judgement_network,
                            pos = vertex_positions,
                            node_size = 3800,
                            node_color = '#73cbf2',
                            alpha = 0.9,
                            edgecolors = '#003459',
                            linewidths = 5,
                            ax = judgement_graph_axes                )
        
        draw_networkx_labels(G = self.comparative_judgement_network,
                            pos = vertex_positions,
                            font_size = 12,
                            font_color = '#003459',
                            font_family = 'Times New Roman',
                            font_weight = 'bold',
                            ax = judgement_graph_axes                               )
        
        
        judgement_graph_edges = {
                                 self.hash_tuple(graph_edge_vertices) : {'graph_edge_vertices' :  graph_edge_vertices,
                                                                          'edge_plot_width' : self.comparative_judgement_network
                                                                                                   [graph_edge_vertices[0]]
                                                                                                   [graph_edge_vertices[1]]
                                                                                                   .get('importance')}
                                 for graph_edge_vertices 
                                 in self.comparative_judgement_network.edges()
                                }
        
        for (graph_edge_hash_desig,
              graph_edge_object    ) in judgement_graph_edges.items():
         
             graph_edge_object.update({
                                      'graph_edge_patch' : draw_networkx_edges(G = self.comparative_judgement_network
                                                                                       .subgraph(nodes = graph_edge_object.get('graph_edge_vertices')),
                                                                              pos = vertex_positions,
                                                                              width = 1.5 * graph_edge_object.get('edge_plot_width'),
                                                                              edge_color = '#002540',
                                                                              node_size = 3600,
                                                                              arrowsize = 18,
                                                                              arrowstyle = '-|>',
                                                                              connectionstyle = 'arc3,rad=0.1',
                                                                              ax = judgement_graph_axes                                                ),
                                    })
             graph_edge_object.update({
                                       'graph_edge_head_coordinates' : apply_coordinate_offset(graph_edge_object.get('graph_edge_patch')
                                                                                                                [0]
                                                                                                                .get_path()
                                                                                                                .vertices
                                                                                                                [2]                      )
                                     })
             graph_edge_object.update({
                                       'graph_edge_intensity_label' : judgement_graph_axes.text(x = graph_edge_object.get('graph_edge_head_coordinates')
                                                                                                                     [0],
                                                                                                y = graph_edge_object.get('graph_edge_head_coordinates')
                                                                                                                     [1],
                                                                                                s = graph_edge_object.get('edge_plot_width'),
                                                                                                fontsize = 20,
                                                                                                fontfamily = 'monospace',
                                                                                                color = '#333333',
                                                                                                style = 'normal',
                                                                                                weight = 'semibold',
                                                                                                horizontalalignment = 'center',
                                                                                                verticalalignment = 'center' 
                                                                                               )
                                     })
        
        
        judgement_graph_axes.margins(0.15)
        judgement_graph_axes.set_axis_off()
        judgement_graph_figure.tight_layout()
        
        self.judgement_graph_plot_axes = {'plot' : judgement_graph_figure,
                                           'axes' : judgement_graph_axes    }
    #
    def calculate_reciprocal_matrix_consistency_index_ratio(self):
                                          
        from pandas import read_csv
        from numpy import real, argmax
        
        self.donegan_dod_random_indices = read_csv(filepath_or_buffer = './data/donegan_dodd_random_indices.csv')
        
        reciprocal_matrix_order = (self.reciprocal_matrix
                                       .shape
                                       [0]                )
        principal_eigenvalue = float(real(self.Λ)[argmax(real(self.Λ))])
        
        consistency_index = ( (principal_eigenvalue - reciprocal_matrix_order)
                             /(reciprocal_matrix_order - 1)                         )
        
        random_index = float(self.donegan_dod_random_indices
                                 .loc[lambda Χ : Χ['matrix_order'] == reciprocal_matrix_order,
                                      'random_index'                                          ]
                                 .squeeze()                                                    )
        
        self.consistency_index_ratio = {'consistency_index' : consistency_index,
                                        'consistency_ratio' : consistency_index/random_index,
                                        'principal_eigenvalue' : principal_eigenvalue,
                                        'reciprocal_matrix_order' : reciprocal_matrix_order    }
        
        return self.consistency_index_ratio
    #
    def construct_hierarchy_model_tournament_graph(self):
    
        self.construct_reciprocal_matrix_from_comparative_judgements()
        self.calculate_priority_vector_from_reciprocal_matrix()
        self.calculate_geometric_mean_priority_vector()
        self.calculate_reciprocal_matrix_consistency_index_ratio()
        self.join_priority_vector_to_reciprocal_matrix()
        self.construct_comparative_judgement_network()
        self.construct_comparative_judgement_network_plot()
        
        return self.reciprocal_matrix_priority_vector
    #


#%%


class calculateStrengthOfAlternativePreference:
    def __init__(self,
                 comparative_judgements = None):
    
        self.comparative_judgements = comparative_judgements
        
        self.orchestrate_strengh_of_preference_calculation()
    #
    def assemble_structural_hierarchy_from_comparative_judgements(self):
    
        self.structural_hierarchy = {
                                      hierarchy_model : calculateHierarchyModelEntropy(comparative_judgements = self.comparative_judgements.loc[hierarchy_model])
                                    
                                       for hierarchy_model
                                       in set(self.comparative_judgements.index)
                                    }
        
        return self.structural_hierarchy.keys()
    #
    def export_hierarchy_model_element_consistency_ratio_to_csv(self):
    
        '''
           Construct `pandas.DataFrame` containing consistency ratios of hierarchy-model 
           comparative judgements. Export as `*.csv`. Rendered as research-paper Table 3.
        '''
        
        from pandas import DataFrame   
        (
            DataFrame.from_dict(
                                data = {
                                         hierarchy_model : ahp_structure.consistency_index_ratio
                                         for (hierarchy_model,
                                              ahp_structure    )
                                         in self.structural_hierarchy.items()
                                         },
                                 orient = 'index'
                                )
                .rename_axis(index = 'hierarchy_model')
                .reset_index(drop = False)
                .sort_values(by = 'hierarchy_model')
                .reset_index(drop = True)
                 .to_csv(path_or_buf = './data/zheng-et-al-reciprocal-matrix-consistency-index-ratio.csv',
                         index = False,
                         encoding = 'utf-8')
        
        )
        
        return '🗂️📂📋📝🖊️'
    #
    def consntruct_priority_vector_table_export_to_csv(self):
    
        '''
           Construct `pandas.DataFrame` containing consistency ratios of hierarchy-model 
           priority vectors. Export as `*.csv`. Rendered as research-paper Table 2.
        '''
        
        from pandas import DataFrame, concat
        
        eigenvector_geometric_mean_priority_vector_comparison = (
                                concat(
                                        objs = {
                                                 hierarchy_model : DataFrame.from_dict(data = {'principal_eigenvector' : ahp_structure.priority_vector,
                                                                                               'geometric_mean' : ahp_structure.geometric_mean_priority_vector})
                                                                            .rename_axis(index = 'hierarchy_element')
                                                                            .reset_index(drop = False)
                                                                            .assign(
                                                                                    hierarchy_model = ahp_structure.hierarchy_model,
                                                                                    hierarchy_element = lambda Ξ : Ξ['hierarchy_element']
                                                                                                                    .apply(func = lambda ξ :   ahp_structure.hierarchy_model
                                                                                                                                             + ':'
                                                                                                                                             + ξ)
                                                                                   )
                                                                            [['hierarchy_model',
                                                                              'hierarchy_element',
                                                                              'principal_eigenvector',
                                                                              'geometric_mean'        ]]
                                                 for (hierarchy_model,
                                                      ahp_structure   )
                                                 in self.structural_hierarchy.items()
                                                 }.values()
                                        )
                            .sort_values(by = ['hierarchy_model',
                                               'hierarchy_element'])
                            .reset_index(drop = True)
                   )
        
        priority_vector_euclidean_distances = (
                                                  eigenvector_geometric_mean_priority_vector_comparison
                                                                  .assign(
                                                                          priority_vector_distance = lambda Χ : Χ[['principal_eigenvector',
                                                                                                                   'geometric_mean'       ]]
                                                                                                                 .apply(func = lambda χ : pow(  χ['principal_eigenvector']
                                                                                                                                              - χ['geometric_mean'],
                                                                                                                                              2                           ),
                                                                                                                        axis = 1                                            )
                                                                         )
                                                                  [['hierarchy_model',
                                                                    'priority_vector_distance']]
                                                                  .groupby(by = 'hierarchy_model',
                                                                           as_index = False        )
                                                                  .sum()
                                                 )
        
        (
         eigenvector_geometric_mean_priority_vector_comparison
                 .merge(right = priority_vector_euclidean_distances)
                 [['hierarchy_model',
                   'hierarchy_element',
                   'principal_eigenvector',
                   'priority_vector_distance']]
                 .sort_values(by = ['hierarchy_model',
                                    'hierarchy_element'])
                 .reset_index(drop = True)
                 .to_csv(path_or_buf = './data/zheng-et-al-priority-vectors.csv',
                         index = False,
                         encoding = 'utf-8')
         )
        
        return eigenvector_geometric_mean_priority_vector_comparison
    #
    def extract_criterion_target_priority_vectors_from_structural_hierarchy(self):
    
        # Extract from dictionary of class objects `structural_hierarchy` priority vectors for
        # each hierarchy model.
        
        self.criterion_alternative_priority_vector = { 
                                                    hierarchy_model : ahp_structure.priority_vector
                                                    for (hierarchy_model,
                                                         ahp_structure    )
                                                    in self.structural_hierarchy.items()
                                                    if hierarchy_model != 'TA_opt'
                                                    
                                                }
        
        self.target_criterion_priority_vector = (self.structural_hierarchy.get('TA_opt')
                                                                .priority_vector)
        
        return (self.criterion_alternative_priority_vector,
                self.target_criterion_priority_vector      )
    #
    def load_alternative_criterion_measurements(self):
    
        from pandas import read_csv
        
        # Construct dictionary of functions to apply [0,1]-standardization to criterion-element
        # measurements conditioned on whether deleterious or beneficial to target objective.
        self.normalize_measurement = {
                                         'deleterious': lambda υ:  (υ - υ.min(axis=1)
                                                                         .to_numpy()
                                                                         [:, None]   ) 
                                                                  /(υ.max(axis=1)
                                                                     .to_numpy()
                                                                     [:, None] - υ.min(axis=1)
                                                                                  .to_numpy()
                                                                                  [:, None]       ),
                                         'beneficial':  lambda χ:  (χ.max(axis=1)
                                                                     .to_numpy()
                                                                     [:, None] - χ)
                                                                  /(χ.max(axis=1)
                                                                     .to_numpy()
                                                                     [:, None] - χ.min(axis=1)
                                                                                  .to_numpy()
                                                                                  [:, None]    )
                                         }
        
        
        # Read in csv file containing raw measurements of each criterion element. Apply
        # Assign column `normalize_measurement` conditioned on value of `effect`, latter
        # of which is dropped.
        self.measurements_staged_for_normalization = (
                                                         read_csv(filepath_or_buffer = './data/zheng-et-al-alternative-criterion-measures.csv',
                                                                  usecols = ['hierarchy_model',
                                                                             'TA3',
                                                                             'TA10',
                                                                             'TA36',
                                                                             'effect'],
                                                                  index_col = 'hierarchy_model')
                                                             .assign(
                                                                     normalize_measurment = lambda Ξ : Ξ['effect']
                                                                                                        .apply(func = lambda ξ : self.normalize_measurement.get(ξ))
                                                                    )
                                                             .drop(columns = ['effect'])
                                                         )
        
        return self.measurements_staged_for_normalization
    #
    def normalize_alternative_criterion_measurements_export_to_csv(self):
    
        from pandas import concat
        
        # Collect dictionary mapping `hierarchy_model` to `normalize_element` from 
        # pandas.DataFrame object `measurements_staged_for_normalization`. 
        self.normalize_measurement = (self.measurements_staged_for_normalization
                                                        ['normalize_measurment']
                                                        .to_dict()               )
        
        self.normalized_measurements = concat(
                                                objs = [
                                                         self.normalize_measurement.get(hierarchy_model)(self.measurements_staged_for_normalization.loc[[hierarchy_model],
                                                                                                                                                        ['TA3',
                                                                                                                                                         'TA10',
                                                                                                                                                         'TA36'  ]        ])
                                                         for hierarchy_model
                                                         in self.measurements_staged_for_normalization.index
                                                        ],
                                                axis = 0                                                                                                                             )
        
        # Export to `csv the `normalized_measurements` pandas.DataFrame object for incorporation into
        # research paper.
        (
          self.normalized_measurements.map(func = lambda υ : round(υ, 4))
                                      .to_csv(path_or_buf = './data/zheng-et-al-normalized-element-measurements.csv',
                                              index = True,
                                              encoding = 'utf-8')
         )
        
        return self.normalized_measurements
    #
    def calculate_strength_of_preference_given_measurements_comparative_judgements(self):
    
        from pandas import DataFrame
        
        self.strength_of_preference = (
                                       DataFrame.from_dict(data = self.criterion_alternative_priority_vector,
                                                           orient = 'columns')
                                                .mul(other = self.normalized_measurements.T)
                                                .dot(other = DataFrame.from_dict(data = self.target_criterion_priority_vector,
                                                                                 orient = 'index')                            )
                                                .rename(columns = {0 : 'preference_strength'})
                                                .sort_values(by = 'preference_strength',
                                                             ascending = False    )
                                     )
        
        return self.strength_of_preference
    #
    def orchestrate_strengh_of_preference_calculation(self):
    
        self.assemble_structural_hierarchy_from_comparative_judgements()
        self.export_hierarchy_model_element_consistency_ratio_to_csv()
        self.consntruct_priority_vector_table_export_to_csv()
        self.extract_criterion_target_priority_vectors_from_structural_hierarchy()
        self.load_alternative_criterion_measurements()
        self.normalize_alternative_criterion_measurements_export_to_csv()
        self.calculate_strength_of_preference_given_measurements_comparative_judgements()
        
        return self.strength_of_preference
    #



#%%


'''
   Read in `*.csv` containing comparative judgements for all hierarchy models
   in Zheng, et al (2015) Table 10 and 
'''

from pandas import read_csv

path_to_judgement_comparison = './data/zheng-et-al-target-criterion-alternative-judgements.csv'

comparative_judgements = (read_csv(filepath_or_buffer = path_to_judgement_comparison)
                            .set_index(keys = 'hierarchy_model',
                                       drop = True              ))


#%%


pref_str = calculateStrengthOfAlternativePreference(comparative_judgements = comparative_judgements)







#%%



ho_b1_judgement_graph_plot = (pref_str.structural_hierarchy
                                      .get('B1')
                                      .judgement_graph_plot_axes
                                      .get('plot')               )


# (
#  ho_mc.judgement_graph_plot_axes.get('plot')
#                                 .savefig(fname = './illustrations/objective_criterion_graph.png',
#                                          dpi = 512,
#                                          transparent = True) 
# )



                                         
#%%




#%%



                                         
#%%




#%%




#%%


#%%






#%%






#%%






#%%
