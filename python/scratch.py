#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:00:34 2026

@author: nahamlet
"""

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
                        node_color = vertex_transparent_face_color,
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
    
    
    self.eliptical_comparative_judgement_plot = {'plot' : judgement_graph_figure_elliptical,
                                                 'axis' : judgement_graph_axes_elliptical   }
    
    return self.eliptical_comparative_judgement_plot
#


