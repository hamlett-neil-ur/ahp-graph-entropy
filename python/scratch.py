#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:00:34 2026

@author: nahamlet
"""

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
        
        return self.bauer_normalized_laplacian
    #





