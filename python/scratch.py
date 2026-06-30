#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:00:34 2026

@author: nahamlet
"""

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
    
    graph_vertex_entropy = {'vertex_entropy' : vertex_probability_entropy,
                            'graph_entropy' : graph_entropy               }
    
    return graph_vertex_entropy
#

