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
        
        
        (self.comparative_judgement_network
             .add_edges_from(
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
        )
        
        self.element_only_vertex_label = {  vertex_label : vertex_label.split(':')
                                                                       [1]
                                            for vertex_label
                                            in self.comparative_judgement_network.nodes() }
        
        return self.comparative_judgement_network.edges()
    #
    def determine_acylicity_of_directed_spanning_subgraph(self):
        
        '''
            Construct a directed spanning subgraph `self.comparative_judgement_network`. 
            Take only the edges from `self.comparative_judgements` for which 
            `reference_factor` > 1. This eliminates all of the undirected edges.
            Apply the resultant edge list to `networkx.DiGraph` object `self.directed_spanning_subgraph`.
            Then apply `networkx.is_directed_acyclic_graph` to `self.directed_spanning_subgraph`.
        '''
    
        from networkx import DiGraph, is_directed_acyclic_graph
        
        self.directed_spanning_subgraph = DiGraph()
        
        (
          self.directed_spanning_subgraph
              .add_edges_from(self.comparative_judgements
                                  .loc[lambda Χ : Χ['importance'] > 1,
                                       ['comparative_factor',
                                        'reference_factor'   ]         ]
                                  .to_records(index = False))
          )
        
        self.directed_spanning_subgraph_acyclicity = {'directed_spanning_subgraph_is_acyclic' : is_directed_acyclic_graph(self.directed_spanning_subgraph),
                                                      'directed_spanning_subgraph' : self.directed_spanning_subgraph}
        
        return self.directed_spanning_subgraph_acyclicity
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
    def construct_elliptical_layout_unlabeled_edge_graph_plot(self):
    
        from numpy import sign, ediff1d
        from networkx import draw_networkx_nodes, draw_networkx_labels,draw_networkx_edges, relabel_nodes, circular_layout
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        from matplotlib.patches import Rectangle, FancyArrow
        
        apply_coordinate_offset = lambda χ : (χ[0] - 0.01 * sign(χ[0]),
                                              χ[1] - 0.03 * sign(χ[1]))
        
        
        
        self.judgement_layout_elliptical = relabel_nodes(G = self.comparative_judgement_network,
                                                             mapping = self.element_only_vertex_label,
                                                             copy = True                                 ) 
        
        circular_node_locus = circular_layout(G = self.judgement_layout_elliptical)
        
        vertex_positions = {
                            digraph_vertex : (4 * circular_locus_coorindate[0],
                                              circular_locus_coorindate[1]     )
                            for (digraph_vertex,
                                 circular_locus_coorindate)
                            in circular_node_locus.items()
                           }
        
        
        (judgement_graph_figure_elliptical,
         judgement_graph_axes_elliptical   ) = plt.subplots(nrows = 1,
                                                 ncols = 1,
                                                 figsize = (5, 2.0))
        
        
        vertex_transparent_face_color = mcolors.to_rgba(c = '#73cbf2',
                                                        alpha = 0.675   )
        draw_networkx_nodes(G = self.judgement_layout_elliptical,
                            pos = vertex_positions,
                            node_size = 375,
                            node_color = [vertex_transparent_face_color],
                            # alpha = 0.75,
                            edgecolors = '#003459',
                            linewidths = 1,
                            ax = judgement_graph_axes_elliptical                )
        
        
        
        judgement_graph_edges = {
                                 self.hash_tuple(graph_edge_vertices) : {'graph_edge_vertices' :  graph_edge_vertices,
                                                                          'edge_plot_width' : self.judgement_layout_elliptical
                                                                                                   [graph_edge_vertices[0]]
                                                                                                   [graph_edge_vertices[1]]
                                                                                                   .get('importance')}
                                 for graph_edge_vertices 
                                 in self.judgement_layout_elliptical.edges()
                                }
        
        draw_networkx_labels(G = self.judgement_layout_elliptical,
                            pos = vertex_positions,
                            font_size = 12,
                            font_color = '#003459',
                            font_family = 'Times New Roman',
                            font_weight = 'bold',
                            ax = judgement_graph_axes_elliptical                               )
        
        
        for (graph_edge_hash_desig,
              graph_edge_object    ) in judgement_graph_edges.items():
            
             graph_edge_object.update({'graph_edge_arrow_size' :      0.05 if graph_edge_object.get('edge_plot_width') == 1
                                                                 else 7.5                                                ,
                                       'graph_edge_color' :      '#23060b' if graph_edge_object.get('edge_plot_width') == 1
                                                            else '#002540'                                                  ,
                                       'graph_edge_weight_factor' :      0.5 if graph_edge_object.get('edge_plot_width') == 1
                                                                    else 0.15,
                                       'graph_edge_linestyle' :      'dashed' if graph_edge_object.get('edge_plot_width') == 1
                                                                else 'solid'
                                       })
         
             graph_edge_object.update({
                                      'graph_edge_patch' : draw_networkx_edges(G = self.judgement_layout_elliptical
                                                                                           .subgraph(nodes = graph_edge_object.get('graph_edge_vertices')),
                                                                              pos = vertex_positions,
                                                                              width = graph_edge_object.get('graph_edge_weight_factor') * graph_edge_object.get('edge_plot_width'),
                                                                              edge_color = graph_edge_object.get('graph_edge_color'),
                                                                              node_size = 375,
                                                                              arrowsize = graph_edge_object.get('graph_edge_arrow_size'),
                                                                              arrowstyle = '-|>',
                                                                              style = graph_edge_object.get('graph_edge_linestyle'),
                                                                              connectionstyle = 'arc3,rad=0.3',
                                                                              ax = judgement_graph_axes_elliptical                                                ),
                                    })
             graph_edge_object.update({
                                       'graph_edge_head_coordinates' : apply_coordinate_offset(graph_edge_object.get('graph_edge_patch')
                                                                                                                [0]
                                                                                                                .get_path()
                                                                                                                .vertices
                                                                                                                [2]                      )
                                     })
        
        judgement_graph_axes_elliptical.margins(y = 0.055     )
        judgement_graph_axes_elliptical.set_xlim(left = judgement_graph_axes_elliptical.get_xlim()[0],
                                                 right = 1.1 * judgement_graph_axes_elliptical.get_xlim()[1])
        
        
        legend_frame_transparent_face_color = mcolors.to_rgba(c = '#d7d2cb',
                                                              alpha = 0.25   )
        
        edge_type_legend_frame = Rectangle(xy = ((  judgement_graph_axes_elliptical.get_xlim()[0] 
                                                 + 0.8 * ediff1d(ary = judgement_graph_axes_elliptical.get_xlim()))[0],
                                                 judgement_graph_axes_elliptical.get_ylim()[0]                     ),
                                           width = (0.185 * ediff1d(ary = judgement_graph_axes_elliptical.get_xlim()))[0],
                                           height = ((0.2 * ediff1d(ary = judgement_graph_axes_elliptical.get_ylim())))[0],
                                           facecolor = legend_frame_transparent_face_color,
                                           edgecolor = '#003459',
                                           linewidth = 1                                                                      )
        directed_edge_legend_patch = FancyArrow(x = edge_type_legend_frame.get_x() + 0.45 * edge_type_legend_frame.get_width(),
                                                y = edge_type_legend_frame.get_y() + 0.25 * edge_type_legend_frame.get_height(),
                                                dx = 0.45 * edge_type_legend_frame.get_width(),
                                                dy = 0,
                                                color = '#002540',
                                                overhang = 0,
                                                linewidth = .675,
                                                head_width = .075 * edge_type_legend_frame.get_height(),
                                               )
        
        judgement_graph_axes_elliptical.add_patch(p = edge_type_legend_frame)
        judgement_graph_axes_elliptical.text(x = edge_type_legend_frame.get_center()[0],
                                             y = edge_type_legend_frame.get_y() + 0.95 * edge_type_legend_frame.get_height(),
                                             s = "graph-edge type",
                                             fontsize = 6,
                                             color = '#003459',
                                             horizontalalignment = 'center',
                                             verticalalignment = 'top'                                                        )
        judgement_graph_axes_elliptical.text(x = edge_type_legend_frame.get_x()+ 0.05 * edge_type_legend_frame.get_width(),
                                             y = edge_type_legend_frame.get_y() + 0.55 * edge_type_legend_frame.get_height(),
                                             s = "undirected",
                                             fontsize = 4,
                                             color = '#003459',
                                             horizontalalignment = 'left',
                                             verticalalignment = 'top'                                                        )
        judgement_graph_axes_elliptical.text(x = edge_type_legend_frame.get_x()+ 0.05 * edge_type_legend_frame.get_width(),
                                             y = edge_type_legend_frame.get_y() + 0.3 * edge_type_legend_frame.get_height(),
                                             s = "directed",
                                             fontsize = 4,
                                             color = '#003459',
                                             horizontalalignment = 'left',
                                             verticalalignment = 'top'                                                        )
        judgement_graph_axes_elliptical.plot([edge_type_legend_frame.get_x() + 0.45 * edge_type_legend_frame.get_width(),
                                               edge_type_legend_frame.get_x() + 0.95 * edge_type_legend_frame.get_width()],
                                              [edge_type_legend_frame.get_y() + 0.5 * edge_type_legend_frame.get_height(),
                                               edge_type_legend_frame.get_y() + 0.5 * edge_type_legend_frame.get_height()],
                                             color = '#23060b',
                                             linestyle = 'dashed',
                                             linewidth = 0.75                                                                 )
        judgement_graph_axes_elliptical.add_patch(p = directed_edge_legend_patch)
        
        judgement_graph_axes_elliptical.set_axis_off()
        judgement_graph_figure_elliptical.tight_layout()
        
        
        self.elliptical_comparative_judgement_plot = {'plot' : judgement_graph_figure_elliptical,
                                                     'axis' : judgement_graph_axes_elliptical   }
        
        return self.elliptical_comparative_judgement_plot
    #
    def construct_judgement_digraph_with_mirror_unit_weighted_edges(self):
    
        self.judgement_network_unit_weight_edges_mirrored = self.comparative_judgement_network.__class__()
        self.judgement_network_unit_weight_edges_mirrored.add_nodes_from(nodes_for_adding = self.comparative_judgement_network
                                                                                                .nodes()                       )
        self.judgement_network_unit_weight_edges_mirrored.add_edges_from(ebunch_to_add = self.comparative_judgement_network
                                                                                            .edges
                                                                                            .data()                           )
        
        
        self.judgement_network_unit_weight_edges_mirrored.add_edges_from(
                                                                         ebunch_to_add =  self.comparative_judgements
                                                                                              .loc[lambda Χ : Χ['importance'] == 1]
                                                                                              .assign(
                                                                                                      comparative_factor = lambda Η : Η['comparative_factor']
                                                                                                                                       .apply(func = lambda η :  self.hierarchy_model
                                                                                                                                                               + ':'
                                                                                                                                                               + η                   ),
                                                                                                      reference_factor = lambda Χ : Χ['reference_factor']
                                                                                                                                     .apply(func = lambda χ :   self.hierarchy_model
                                                                                                                                                              + ':'
                                                                                                                                                              + χ                    ),
                                                                                                      importance = lambda Ξ : Ξ['importance']
                                                                                                                               .apply(func = lambda ξ : {'importance' : ξ})
                                                                                                   )
                                                                                              [['reference_factor',
                                                                                                'comparative_factor',
                                                                                                'importance'        ]]
                                                                                              .to_records(index = False)
                                                                        )
        
        return (self.judgement_network_unit_weight_edges_mirrored
                        .edges
                        .data()                                   )
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
    def calculate_vertex_edge_weight_graph_entropy(self):
    
        from pandas import DataFrame
        from math import log2
        
        out_edge_importance = (
                                DataFrame(data = self.judgement_network_unit_weight_edges_mirrored
                                                     .edges
                                                     .data(),
                                          columns = ['comparative_factor',
                                                     'reference_factor',
                                                     'importance'        ]                         )
                                    .assign(importance = lambda Ξ : Ξ['importance']
                                                                     .apply(func = lambda ξ : ξ.get('importance')))
                              )
        
        vertex_probability_entropy = (
                                      out_edge_importance
                                          .merge(right = out_edge_importance
                                                              [['comparative_factor',
                                                                'importance'         ]]
                                                              .groupby(by = 'comparative_factor',
                                                                       as_index = False          )
                                                              .sum()
                                                              .rename(columns = {'importance' : 'net_out_edge_importance'}))
                                          .assign(
                                                  vertex_probability = lambda Η : Η.apply(func = lambda η :  η['importance']
                                                                                                            /η['net_out_edge_importance'],
                                                                                          axis = 1                                         ),
                                                  vertex_entropy = lambda Χ : Χ['vertex_probability']
                                                                               .apply(func = lambda χ : -χ * log2(χ))
                                                 )
                                          [['comparative_factor',
                                            'vertex_probability',
                                            'vertex_entropy']]
                                    )
        
        graph_entropy = float(
                              vertex_probability_entropy
                                 .set_index(keys = 'comparative_factor',
                                            drop = True                 )
                                 ['vertex_entropy']
                                 .sum()
                              )
        
        self.graph_vertex_entropy = {'vertex_entropy' : vertex_probability_entropy,
                                     'graph_entropy' : graph_entropy               }
        
        return self.graph_vertex_entropy
    #
    def construct_weighted_hermitian_adjacency_matrix(self):
    
        from networkx import compose
        from pandas import DataFrame
        # After:
        # [1] Yu, Geng, Zhou (2023) https://doi.org/10.1016/j.disc.2022.113254.
        # [2] Wang, Z; She, T.; Wang, C. (2024) http://dx.doi.org/10.61091/um119-07.
        
        mirrored_edge_judgement_network = (self.comparative_judgement_network
                                               .__class__()                   )
        complex_weighted_edge_judgment_network = (self.comparative_judgement_network
                                                      .__class__()                   )
        complex_weighted_edge_judgment_network.add_edges_from(ebunch_to_add = self.comparative_judgement_network
                                                                                  .edges(data = True)           )
        mirrored_edge_judgement_network.add_edges_from(ebunch_to_add = self.comparative_judgement_network
                                                                           .reverse()
                                                                           .edges
                                                                           .data()                       )
        
        for (comparative_element,
             reference_element,
             edge_importance      ) in mirrored_edge_judgement_network.edges(data = True):
            mirrored_edge_judgement_network.edges[comparative_element,
                                                  reference_element   ]['importance'] = (   edge_importance['importance']
                                                                                         if edge_importance['importance'] == 1
                                                                                         else -1j * edge_importance['importance'])
        for (comparative_element,
             reference_element,
             edge_importance      ) in complex_weighted_edge_judgment_network.edges(data = True):
            complex_weighted_edge_judgment_network.edges[comparative_element,
                                                         reference_element]['importance'] = (   edge_importance['importance']
                                                                                             if edge_importance['importance'] == 1
                                                                                             else 1j * edge_importance['importance'])
        
        weighted_hermitian_adjacency_matrix = (
                                                DataFrame(data = compose(G = mirrored_edge_judgement_network,
                                                                         H = complex_weighted_edge_judgment_network).edges(data = True),
                                                          columns = ['comparative_element',
                                                                     'reference_element',
                                                                     'importance_intensity'])
                                                   .assign(importance_intensity = lambda Ξ : Ξ['importance_intensity']
                                                                                              .apply(func = lambda ξ : str(ξ.get('importance'))))
                                                   .pivot(columns = 'comparative_element',
                                                          index = 'reference_element',
                                                          values = 'importance_intensity')
                                                   .astype(dtype = complex)
                                                   .fillna(value = 0)
                                                )
        
        self.weighted_hermetian_adjacency = {'weighted_hermitian_adjacency_matrix' : weighted_hermitian_adjacency_matrix,
                                             'mirrored_edge_judgement_network' : mirrored_edge_judgement_network,
                                             'complex_weighted_edge_judgment_network' : complex_weighted_edge_judgment_network }
        
        return self.weighted_hermetian_adjacency
    #
    def calculate_comparative_judgement_edge_weight_entropy(self):
    
        from networkx import compose
        from pandas import DataFrame
        from math import log2
        # After:
        # Chen, et al (2015) https://doi.org/10.3390/e17063710.
        # Fung (2025) https://doi.org/10.1007/s00026-005-0237-z.
        
        zero_weight_mirrored_edge_judgement_network = (self.comparative_judgement_network
                                                           .__class__()                   )
        judgment_network_replica = (self.comparative_judgement_network
                                        .__class__()                   )
        zero_weight_mirrored_edge_judgement_network.add_edges_from(ebunch_to_add = self.comparative_judgement_network
                                                                                       .reverse()
                                                                                       .edges(),
                                                                   importance = 0                                     )
        judgment_network_replica.add_edges_from(ebunch_to_add = self.comparative_judgement_network
                                                                    .edges(data = True)           )
        
        judgement_network_zero_weighted_mirror = compose(G = zero_weight_mirrored_edge_judgement_network,
                                                         H = judgment_network_replica                    )
        
        
        vertex_by_neighbors = {graph_vertex : sorted(list(self.judgement_network_unit_weight_edges_mirrored
                                                              .to_undirected()
                                                              .neighbors(n = graph_vertex)                 ))
                               for graph_vertex
                               in self.judgement_network_unit_weight_edges_mirrored
                                      .nodes()                                                                }
        incident_edge_weight_by_vertex = {graph_vertex : {adjacent_vertex : judgement_network_zero_weighted_mirror
                                                                                  .get_edge_data(u = graph_vertex,
                                                                                                 v = adjacent_vertex)
                                                                                  .get('importance')
                                                          for adjacent_vertex
                                                          in vertex_by_neighbors.get(graph_vertex)                  }
                                           for graph_vertex
                                           in vertex_by_neighbors.keys()                                               }
        aggregate_incident_weight_by_vertex = {graph_vertex : sum(incident_edge_weights.values())
                                               for (graph_vertex,
                                                    incident_edge_weights)
                                               in incident_edge_weight_by_vertex.items()         }
        
        # Fung (2025) interprets this as a set of state-transition probabilities.
        normalized_incident_edge_weights = {
                                              graph_vertex : {adjacent_vertex : connecting_edge_weight
                                                                                / (   1 
                                                                                   if aggregate_incident_weight_by_vertex.get(graph_vertex) == 0
                                                                                   else aggregate_incident_weight_by_vertex.get(graph_vertex)   )
                                                              for (adjacent_vertex,
                                                                   connecting_edge_weight)
                                                              in incident_edge_weights.items()
                                                             }
                                              for (graph_vertex,
                                                   incident_edge_weights)
                                              in incident_edge_weight_by_vertex.items()
                                             }
        
        incident_edge_probability_entropy = (
                                             DataFrame.from_dict(data = normalized_incident_edge_weights,
                                                                 orient = 'index')
                                                      .rename_axis(index = 'graph_vertex' )
                                                      .reset_index(drop = False)
                                                      .melt(id_vars = 'graph_vertex',
                                                            var_name = 'adacent_vertex',
                                                            value_name = 'edge_probability')
                                                      .dropna(axis = 0,
                                                              how = 'any')
                                                      .assign(
                                                              edge_entropy = lambda Ξ : Ξ['edge_probability']
                                                                                         .apply(func = lambda ξ :      1 if ξ == 0
                                                                                                                  else - log2(ξ) * ξ)
                                                             )
                                             )
        
        self.edge_weight_entropy = float(incident_edge_probability_entropy['edge_entropy']
                                                                           .sum()          )
        self.edge_weight_entropy_build_up = {'incident_edge_probability_entropy' : incident_edge_probability_entropy,
                                              'incident_edge_weight_by_vertex' : incident_edge_weight_by_vertex,
                                              'normalized_incident_edge_weights' : normalized_incident_edge_weights,
                                              'aggregate_incident_weight_by_vertex' : aggregate_incident_weight_by_vertex }
        
        return self.edge_weight_entropy
    #
    def construct_comparative_judgement_transition_probability_matrix(self):
    
        from networkx import  DiGraph
        from pandas import DataFrame
        from scipy.linalg import eig
        
        # After:  Chung (2005) https://doi.org/10.1007/s00026-005-0237-z
        # 
        # Chung (2005) offers a graph-Laplacian approach based strictly on edge weights.
        # Edge weights are interpreted as bases for state-transition probabilities. To construct,
        # we begin with `self.judgement_network_unit_weight_edges_mirrored` constructed by method
        # `construct_judgement_digraph_with_mirror_unit_weighted_edges`. Some graph algebra
        # produces an edge-list complement, for which the `intensity_of_importance` weights
        # are the reciprocals of those in the our baseline.
        
        self.chung_laplacian_network_base = (self.judgement_network_unit_weight_edges_mirrored
                                                 .__class__()                                   )
        self.chung_laplacian_network_base.add_edges_from(ebunch_to_add = self.judgement_network_unit_weight_edges_mirrored
                                                                             .edges(data = True)                            )
        unit_weight_edge_mirrored_compliment = DiGraph()
        unit_weight_edge_mirrored_compliment.add_edges_from(ebunch_to_add = (
                                                                             DataFrame(data = self.judgement_network_unit_weight_edges_mirrored
                                                                                                   .edges(data = True                           ),
                                                                                       columns = ['reference_factor',
                                                                                                  'comparative_factor',
                                                                                                  'intensity_of_importance']                      )
                                                                                 .loc[lambda Ξ : Ξ['intensity_of_importance']
                                                                                                  .apply(func = lambda ξ : ξ.get('importance') != 1)]
                                                                                 .assign(intensity_of_importance = lambda Η : Η['intensity_of_importance']
                                                                                                                               .apply(func = lambda η : {'importance' : 1/η.get('importance')}))
                                                                                 .to_records(index = False)
                                                                            )
                                                                                                                                                                                                    )
        self.chung_laplacian_network_base.add_edges_from(ebunch_to_add = unit_weight_edge_mirrored_compliment.reverse()
                                                                                                              .edges(data = True))
        comparative_judgement_transition_edge_weight_explicit = (
                                                                 DataFrame(data = self.chung_laplacian_network_base
                                                                                       .edges(data = True           ),
                                                                           columns = ['comparative_factor',
                                                                                      'reference_factor',
                                                                                      'intensity_of_importance']     )
                                                                     .assign(intensity_of_importance = lambda Χ : Χ['intensity_of_importance']
                                                                                                                   .apply(func = lambda χ : χ.get('importance')))
                                                                     .sort_values(by = ['comparative_factor',
                                                                                        'reference_factor'   ])
                                                                     .reset_index(drop = True)
                                                                 )
        
        vertex_in_degree_volume = (
                                   comparative_judgement_transition_edge_weight_explicit
                                        [['reference_factor',
                                          'intensity_of_importance']]
                                        .groupby(by = ['reference_factor'],
                                                 as_index = False          )
                                        .sum()
                                        .assign(vertex_in_degree_volume = lambda Η : Η['intensity_of_importance']
                                                                                      .apply(func = lambda η :      1 if η ==  0
                                                                                                               else η           ))
                                        [['reference_factor',
                                          'vertex_in_degree_volume']]
                                        .sort_values(by = 'reference_factor')
                                        .reset_index(drop = True)
                                     )
        self.comparative_judgement_transition_probability_matrix = (
                                                                    comparative_judgement_transition_edge_weight_explicit
                                                                        .merge(right = vertex_in_degree_volume)
                                                                        .assign(vertex_transition_probability = lambda Χ : Χ['intensity_of_importance']
                                                                                                                            .div(other = Χ['vertex_in_degree_volume']))
                                                                        .pivot(index = 'reference_factor',
                                                                               columns = 'comparative_factor',
                                                                               values = 'vertex_transition_probability')
                                                                        .fillna(value = 0)
                                                                   )
        (Λ,
         Χ) = eig(self.comparative_judgement_transition_probability_matrix)
        
        self.comparative_judgement_transition_probability = {
                'comparative_judgement_transition_probability_matrix' : self.comparative_judgement_transition_probability_matrix,
                'chung_laplacian_network_base' : self.chung_laplacian_network_base,
                'Χ' : Χ,
                'Λ' : Λ
            }
        
        return self.comparative_judgement_transition_probability_matrix
    #
    def construct_edge_weight_digraph_bases_for_bauer_laplacian(self):
    
        from networkx import difference, complete_graph, DiGraph, set_edge_attributes, compose
        
        # After: Bauer (2012) http://dx.doi.org/10.1016/j.laa.2012.01.020.
        # Construct from the comparative-judgement graph a digraph conforming to the
        # Bauer (2012) convention, in which edge-weight values contain all graph-
        # connectivity information. 
        # ⓵ Begin with the `self.judgement_network_unit_weight_edges_mirrored`
        #    attribute constructed by method 
        #    `construct_judgement_digraph_with_mirror_unit_weighted_edges`.
        #    This contains all of comparative-judgement information. 
        # ⓶ Constructed an edge-complement DiGraph object. 
        #    ⓐ Construct a complete DiGraph based on the nodes in 
        #       `self.judgement_network_unit_weight_edges_mirrored`. This 
        #       complete DiGraph is not a tournament graph in the sence of
        #       Brown, et al (2020) https://doi.org/10.1016/j.laa.2019.09.026,
        #       containing only a single directed edge between each vertex pair.
        #       Our "complete" DiGraph contains mirror edges — one in each direction —
        #       for each vertex pair.
        #    ⓑ The desired `unit_weight_edge_mirrored_edge_complement` DiGraph object
        #       is the edge difference between the complete graph in ⓐ and our
        #       DiGraph attribute `self.judgement_network_unit_weight_edges_mirrored`.
        #    ⓒ Set ⟪{'importance' : 0}⟫ edge-weight attributes for each edge in our
        #       `unit_weight_edge_mirrored_edge_complement` DiGraph object.
        # ⓷ Our desired DiGraph object `bauer_laplacian_basis_graph` results from the
        #    composition of `unit_weight_edge_mirrored_edge_complement` with
        #    `self.judgement_network_unit_weight_edges_mirrored`.
        
        
        unit_weight_edge_mirrored_edge_complement = difference(
                                                               G = complete_graph(n = self.judgement_network_unit_weight_edges_mirrored.nodes(),
                                                                                  create_using = DiGraph()                                       ),
                                                               H = self.judgement_network_unit_weight_edges_mirrored
                                                              )
        set_edge_attributes(G = unit_weight_edge_mirrored_edge_complement, 
                            values = 0,
                            name = 'importance'                           )
        
        self.bauer_laplacian_basis_graph = compose(G = self.judgement_network_unit_weight_edges_mirrored,
                                                   H = unit_weight_edge_mirrored_edge_complement           )
        
        return self.bauer_laplacian_basis_graph.edges(data = True)
    #
    def construct_bauer_normalized_laplacian(self):
    
        from pandas import DataFrame
        from numpy import diag, identity
        from scipy.linalg import eig
        
        # After: Bauer (2012) http://dx.doi.org/10.1016/j.laa.2012.01.020.
        # 
        # Bauer (2012) constructs a Laplacian in terms of the directed-graph incidence matrix
        # (Brouwer & Haemers, 2012, https://doi.org/10.1007/978-1-4614-1939-6). Instead of
        # the cardinality of incident edges on which Brower's & Haemers' (2012) definition is based,
        # Bauer (2012) employs the sum of the 
        
        bauer_graph_edge_weight_matrix = (
                                          DataFrame(data = self.chung_laplacian_network_base
                                                                .edges(data = True),
                                                    columns = ['comparative_element',
                                                               'reference_element',
                                                               'intensity_of_importance']     )
                                              .assign(intensity_of_importance = lambda Ξ : Ξ['intensity_of_importance']
                                                                                            .apply(func = lambda ξ : ξ.get('importance')))
                                              .pivot(index = 'comparative_element',
                                                     columns = 'reference_element',
                                                     values = 'intensity_of_importance'  )
                                              .fillna(value = 0)
                                         )
        inverse_vertex_in_degree = DataFrame(data = diag(v = bauer_graph_edge_weight_matrix.sum(axis = 1)
                                                                                           .map(func = lambda χ :      0 if χ == 0
                                                                                                                  else 1/χ         )),
                                             columns = bauer_graph_edge_weight_matrix.columns,
                                             index = bauer_graph_edge_weight_matrix.index                                            )
        identity_matrix = DataFrame(data = identity(n = bauer_graph_edge_weight_matrix.shape[0]),
                                    columns = bauer_graph_edge_weight_matrix.columns,
                                    index = bauer_graph_edge_weight_matrix.index                 )
        self.bauer_normalized_laplacian = (identity_matrix.sub(other = inverse_vertex_in_degree.dot(other = bauer_graph_edge_weight_matrix)))
        
        (Λ_bauer,
         Χ_bauer ) = eig(self.bauer_normalized_laplacian)
        
        self.bauer_lapacian_construction = {
                        'bauer_normalized_laplacian' : self.bauer_normalized_laplacian,
                        'bauer_graph_edge_weight_matrix' : bauer_graph_edge_weight_matrix,
                        'Λ' : Λ_bauer,
                        'Χ' : Χ_bauer                                                      }
        
        return self.bauer_normalized_laplacian
    #
    def construct_hierarchy_model_tournament_graph(self):
    
        self.construct_reciprocal_matrix_from_comparative_judgements()
        self.calculate_priority_vector_from_reciprocal_matrix()
        self.calculate_geometric_mean_priority_vector()
        self.calculate_reciprocal_matrix_consistency_index_ratio()
        self.join_priority_vector_to_reciprocal_matrix()
        self.construct_comparative_judgement_network()
        self.determine_acylicity_of_directed_spanning_subgraph()
        self.construct_comparative_judgement_network_plot()
        self.construct_elliptical_layout_unlabeled_edge_graph_plot()
        
        self.construct_judgement_digraph_with_mirror_unit_weighted_edges()
        self.calculate_vertex_edge_weight_graph_entropy()
        self.construct_weighted_hermitian_adjacency_matrix()
        self.calculate_comparative_judgement_edge_weight_entropy()
        self.construct_comparative_judgement_transition_probability_matrix()
        self.construct_bauer_normalized_laplacian()
        
        return self.edge_weight_entropy
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
    def construct_priority_vector_table_export_to_csv(self):
    
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
    
        self.criterion_alternative_priority_vector = {  hierarchy_model : ahp_structure.priority_vector
                                                        for (hierarchy_model,
                                                             ahp_structure    )
                                                        in self.structural_hierarchy.items()
                                                        if hierarchy_model != 'TA_opt'                   }
        self.target_criterion_priority_vector = (self.structural_hierarchy.get('TA_opt')
                                                                .priority_vector)
        return (self.criterion_alternative_priority_vector,
                self.target_criterion_priority_vector      )

    def load_alternative_criterion_measurements(self):
    
        from pandas import read_csv
        
        self.normalize_measurement = {  'beneficial' : lambda υ:  (υ - υ.min(axis=1)
                                                                         .to_numpy()
                                                                         [:, None]   ) 
                                                                  /(υ.max(axis=1)
                                                                     .to_numpy()
                                                                     [:, None] - υ.min(axis=1)
                                                                                  .to_numpy()
                                                                                  [:, None]       ),
                                         'deleterious' :  lambda χ:  (χ.max(axis=1)
                                                                     .to_numpy()
                                                                     [:, None] - χ)
                                                                  /(χ.max(axis=1)
                                                                     .to_numpy()
                                                                     [:, None] - χ.min(axis=1)
                                                                                  .to_numpy()
                                                                                  [:, None]    )  }
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
        self.construct_priority_vector_table_export_to_csv()
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


ho_TAopt = (pref_str.structural_hierarchy
                    .get('TA_opt')               )
ho_B1 = (pref_str.structural_hierarchy
                 .get('B1')               )

# (
#    ho_TAopt.elliptical_comparative_judgement_plot
#            .get('plot')
#            .savefig(fname = './illustrations/zheng-target-criterion-judgement-graph.png',
#                     transparent = True,
#                     bbox_inches = 'tight',
#                     dpi = 512                                                             )
#  )



#%%

from networkx import complete_graph, adjacency_matrix, random_regular_graph
from scipy.sparse.linalg import eigs
from numpy import identity, diagflat, array

vertex_count = 5
graph_regularity = 2
exemplary_complete_graph = complete_graph(n = vertex_count)
exemplary_regular_graph = random_regular_graph(d = graph_regularity,
                                               n = vertex_count      )
complete_graph_adjacency = adjacency_matrix(G = exemplary_complete_graph)
vertex_degree_digonal = diagflat(v = [vertex_degree
                                      for (vertex_label,
                                           vertex_degree)
                                      in exemplary_complete_graph.degree])

eigs(A = complete_graph_adjacency.toarray(),
     which = 'LM')

eigs(A = vertex_degree_digonal - complete_graph_adjacency,
     which = 'LM')


#%%

type(complete_graph_adjacency.toarray())




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
