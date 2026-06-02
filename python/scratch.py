#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:00:34 2026

@author: nahamlet
"""

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

