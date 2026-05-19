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
                             'angle' : 'θ'             }


#%%

ho_mc = calculateHierarchyModelEntropy(comparative_judgements = judgement_comparison.loc['objective_criterion']
                                                                                    .reset_index(drop = True)   )

ho_mc.construct_reciprocal_matrix_from_comparative_judgements()
ho_mc.calculate_priority_vector_from_reciprocal_matrix()
ho_mc.join_priority_vector_to_reciprocal_matrix()
ho_mc.construct_comparative_judgement_network()


#%%

from networkx import circular_layout, draw_networkx_nodes, draw_networkx_labels,draw_networkx_edges
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

times_bold_italic = FontProperties(
    family='Times New Roman',
    weight='bold',
    style='italic'
)

#%%




#%%

(judgement_graph_figure,
 judgement_graph_axes   ) = plt.subplots(nrows = 1,
                                         ncols = 1,
                                         figsize = (5, 3.75))

vertex_positions  = circular_layout(G = ho_mc.comparative_judgement_network)
edge_widths = [ho_mc.comparative_judgement_network
                    [edge_tail]
                    [edge_head]
                    .get('importance')
               for (edge_tail,
                    edge_head)
               in ho_mc.comparative_judgement_network
                       .edges()                        ]

draw_networkx_edges(G = ho_mc.comparative_judgement_network,
                    pos = vertex_positions,
                    width = edge_widths,
                    edge_color = '#333333',
                    node_size = 3600,
                    arrowsize = 18,
                    arrowstyle = '-|>',
                    connectionstyle = 'arc3,rad=0.1',
                    ax = judgement_graph_axes       )
draw_networkx_nodes(G = ho_mc.comparative_judgement_network,
                    pos = vertex_positions,
                    node_size = 3600,
                    node_color = '#73cbf2',
                    alpha = 0.9,
                    edgecolors = '#003459',
                    linewidths = 5,
                    ax = judgement_graph_axes)


draw_networkx_labels(G = ho_mc.comparative_judgement_network,
                     pos = vertex_positions,
                     labels = {vertex_label : vertex_abbreviation
                               for (vertex_label,
                                    vertex_abbreviation)
                               in judgement_graph_label_map.items()
                               if vertex_label 
                               in ho_mc.comparative_judgement_network
                                       .nodes()                       },
                     font_size = 16,
                     font_color = '#003459',
                     font_family = 'Times New Roman',
                     font_weight = 'bold',
                     ax = judgement_graph_axes                               )

judgement_graph_axes.margins(0.20)
judgement_graph_axes.set_axis_off()
judgement_graph_figure.tight_layout()
judgement_graph_figure.savefig(fname = './illustrations/objective_criterion_graph.png',
                               dpi = 512,
                               transparent = True)


#%%






#%%






#%%






#%%






#%%






#%%






#%%






#%%
