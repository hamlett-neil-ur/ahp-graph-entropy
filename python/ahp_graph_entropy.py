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
        
        self.construct_hierarchy_model_tournament_graph()
    
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
                                                                  .assign(importance = lambda Ξ : Ξ['importance']
                                                                                                   .apply(func = lambda ξ : {'importance' : ξ}))
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
        
        (judgement_graph_figure,
         judgement_graph_axes   ) = plt.subplots(nrows = 1,
                                                 ncols = 1,
                                                 figsize = (5, 3.75))
        
        
        vertex_positions  = circular_layout(G = self.comparative_judgement_network)
        edge_widths = [self.comparative_judgement_network
                            [edge_tail]
                            [edge_head]
                            .get('importance')
                       for (edge_tail,
                            edge_head)
                       in self.comparative_judgement_network
                               .edges()                        ]
        
        graph_edges = draw_networkx_edges(G = self.comparative_judgement_network,
                                          pos = vertex_positions,
                                          width = list(map(lambda ι : 1.25 * ι,
                                                           edge_widths          )),
                                          edge_color = '#002540',
                                          node_size = 3600,
                                          arrowsize = 18,
                                          arrowstyle = '-|>',
                                          connectionstyle = 'arc3,rad=0.1',
                                          ax = judgement_graph_axes                 )
        draw_networkx_nodes(G = self.comparative_judgement_network,
                            pos = vertex_positions,
                            node_size = 3600,
                            node_color = '#73cbf2',
                            alpha = 0.9,
                            edgecolors = '#003459',
                            linewidths = 5,
                            ax = judgement_graph_axes                )
        
        
        graph_label_text = draw_networkx_labels(G = self.comparative_judgement_network,
                                                pos = vertex_positions,
                                                labels = {vertex_label : vertex_abbreviation
                                                          for (vertex_label,
                                                               vertex_abbreviation)
                                                          in judgement_graph_label_map.items()
                                                          if vertex_label 
                                                          in self.comparative_judgement_network
                                                                  .nodes()                       },
                                                font_size = 24,
                                                font_color = '#003459',
                                                font_family = 'Times New Roman',
                                                font_weight = 'bold',
                                                ax = judgement_graph_axes                               )
        
        graph_edge_head_coordinates = {edge_width : apply_coordinate_offset(arrow_patch.get_path()
                                                                                       .vertices
                                                                                       [2])
                                       for (edge_width,
                                            arrow_patch)
                                       in dict(zip(edge_widths,
                                                   graph_edges))
                                                 .items()                              } 
        
        for (edge_weight,
             edge_head_offset) in graph_edge_head_coordinates.items():
            judgement_graph_axes.text(x = edge_head_offset[0],
                                      y = edge_head_offset[1],
                                      s = edge_weight,
                                      fontsize = 20,
                                      fontfamily = 'monospace',
                                      color = '#333333',
                                      style = 'normal',
                                      weight = 'semibold',
                                      horizontalalignment = 'center',
                                      verticalalignment = 'center'    )
        
        judgement_graph_axes.margins(0.15)
        judgement_graph_axes.set_axis_off()
        judgement_graph_figure.tight_layout()
        # judgement_graph_figure.savefig(fname = './illustrations/objective_criterion_graph.png',
        #                                dpi = 512,
        #                                transparent = True)
        
        self.judgement_graph_plot_axes = {'plot' : judgement_graph_figure,
                                           'axes' : judgement_graph_axes    }
        
        return self.judgement_graph_plot_axes
    #
    def construct_hierarchy_model_tournament_graph(self):
    
        self.construct_reciprocal_matrix_from_comparative_judgements()
        self.calculate_priority_vector_from_reciprocal_matrix()
        self.join_priority_vector_to_reciprocal_matrix()
        self.construct_comparative_judgement_network()
        self.construct_comparative_judgement_network_plot()
        
        return self.reciprocal_matrix_priority_vector
    #


#%%



#%%


from pandas import read_csv

path_to_judgement_comparison = './data/bu-et-al-pemfc-judgement-comparison.csv'

judgement_comparison = (read_csv(filepath_or_buffer = path_to_judgement_comparison)
                            .set_index(keys = 'hierarchy_model',
                                       drop = True              ))

judgement_graph_label_map = {'current_density' : 'I',
                             'oxygen_uniformity' : 'UI',
                             'pressure_drop' : 'ΔP',
                             'height' : 'H',
                             'width' : 'W',
                             'angle' : 'θ',
                             'objective_criterion' : 'O-C',
                             'criterion_pressure_drop' : 'C-ΔP',
                             'criterion_oxygen_uniformity' : 'C-UI',
                             'criterion_current_desnsity' : 'C-I',
                             'priority_vector' : 'ωᵢ',
                             'reference_factor' : 'element'
                             }



#%%

structural_hierarchy = {
                          hierarchy_model : calculateHierarchyModelEntropy(comparative_judgements = judgement_comparison.loc[hierarchy_model]
                                                                                                              .reset_index(drop = True)   )
                        
                           for hierarchy_model
                           in set(judgement_comparison.index)
                        }
ho_mc = structural_hierarchy.get('objective_criterion')



#%%

# (
#  ho_mc.judgement_graph_plot_axes.get('plot')
#                                 .savefig(fname = './illustrations/objective_criterion_graph.png',
#                                          dpi = 512,
#                                          transparent = True) 
# )


#%%

from pandas import concat
(
    concat(
           objs = [
                  structural_hierarchy.get(hierarchy_model)
                                      .reciprocal_matrix_priority_vector
                                      .assign(hierarchy_model = judgement_graph_label_map.get(hierarchy_model),
                                              reference_factor = lambda Ξ : Ξ['reference_factor']
                                                                             .map(func = judgement_graph_label_map))
                                      .rename(columns = judgement_graph_label_map)
                  for hierarchy_model 
                  in set(judgement_comparison.index)
                  if hierarchy_model != 'objective_criterion'
                 ]
                )
    [['hierarchy_model',
      'element',
      'θ',
      'H',
      'W',
      'ωᵢ'              ]]
    .sort_values(by = ['hierarchy_model',
                       'element'          ])
    .reset_index(drop = True)
    .to_csv(path_or_buf = './data/bu-et-al-pmefc-recip-mtx-pri-vec.csv',
            index = False,
            encoding = 'utf-8')
)



#%%

from numpy import real, max
from pandas import DataFrame

consistency_indices = {
                          hierarchy_model : {'perron_value' : float(max(real(ahp_construction.Λ))),
                                             'reciprocal_matrix_order' : ahp_construction.reciprocal_matrix
                                                                                       .shape[0]           }
                          for (hierarchy_model,
                               ahp_construction)
                          in structural_hierarchy.items()
                         }

for (hierarchy_model,
     index_components) in consistency_indices.items():
    index_components.update({'consistency_index' :  (index_components.get('perron_value') - index_components.get('reciprocal_matrix_order'))
                                                   /(index_components.get('reciprocal_matrix_order') - 1)})
    index_components.update({'consistency_ratio' :  index_components.get('consistency_index')/0.4887})


(
    DataFrame.from_dict(data = consistency_indices,
                        orient = 'index'           )
        .rename_axis(index = 'hierarchy_model')
        .reset_index(drop = False)
        .to_csv(path_or_buf = './data/bu-et-al-pmefc-consistency-indices.csv',
                index = False,
                encoding = 'utf-8')
)

#%%

from pandas import DataFrame, read_csv

objective_priority_vector = (
                                DataFrame.from_dict(
                                                     data = structural_hierarchy.get('objective_criterion')
                                                                         .priority_vector,
                                                     orient = 'index'
                                                    )
                                        .rename(index = judgement_graph_label_map)
                                        .rename(index = lambda ξ : 'C-' + ξ)
                                        .rename(columns = {0 : 'O-C'})
                            )

constituent_priority_vectors = (
                                   DataFrame.from_dict(data = {
                                                                 judgement_graph_label_map.get(hierarchy_model) : ahp_construction.priority_vector
                                                                 for (hierarchy_model,
                                                                      ahp_construction)
                                                                 in structural_hierarchy.items()
                                                                 if hierarchy_model != 'objective_criterion'
                                                             },
                                                       orient = 'columns'
                                                      )
                                           .rename(index = judgement_graph_label_map)
                                           # .to_numpy()
                                )

geometric_parameters = (
                         read_csv(filepath_or_buffer = './data/bu-et-al-pemfc-design-paramter-range.csv',
                                  usecols = ['θ',
                                             'H',
                                             'W']                                                         )
                        
                         )

normalized_geometric_parameters = (geometric_parameters - geometric_parameters.min()).div(other = geometric_parameters.max() - geometric_parameters.min())


# Influences of geometric parameters on operating parameters. Combines geometric-parameter priority vectors with
# with priority vectors for operating parameters. Priority vectors in both cases result from the principal
# eigenvectors resulting from each hierarchy model's reciprocal matrix.
constituent_priority_vectors.dot(other = objective_priority_vector)



#%%


from pandas import read_csv
from numpy import log

# `R` min-max scaling. Misnamed `Z` in (16), (32).
normalized_operating_parameters = (
                                      read_csv(filepath_or_buffer = './data/bu-et-al-pemfc-design-paramter-range.csv',
                                               usecols = ['I',
                                                          'ΔP',
                                                          'UI']                                                         )
                                          .assign(
                                                  I = lambda Ξ : Ξ['I']
                                                                  .apply(func = lambda ξ :  (ξ - Ξ['I'].min())
                                                                                           /(Ξ['I'].max()-Ξ['I'].min())),
                                                  ΔP = lambda Η : Η['ΔP']
                                                                   .apply(func = lambda η :  (Η['ΔP'].max()-η)
                                                                                            /(Η['ΔP'].max()-Η['ΔP'].min())),
                                                  UI = lambda Χ : Χ['UI']
                                                                   .apply(func = lambda χ :  (Χ['UI'].max() - χ)
                                                                                            /(Χ['UI'].max() - Χ['UI'].min()))
                                                 )
                                     )


# `P`. (33) Column-sum-normalized `R`. 
performance_proportion = normalized_operating_parameters.div(other = normalized_operating_parameters.sum())


# `eⱼ` for the individual factors in `P`. Calculated as (17).
# Reproduces first row table 13.
element_entropy = (
                     -(performance_proportion + 1e-12)
                         .mul(other = (performance_proportion + 1e-12)
                                          .map(func = log)
                                                                      )
                         .sum()
                         /log(performance_proportion.shape[0])
                    )

# Entropy weight `ωⱼ` from (18). Reproduces second row table 13.
ω_entropy = (1 - element_entropy)/(1 - element_entropy).sum()


# AHP-Entropy Weight Cross.
performance_proportion.mul(other = ω_entropy)


#%%






#%%






#%%






#%%
