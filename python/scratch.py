#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:00:34 2026

@author: nahamlet
"""

def determine_acylicity_of_directed_spanning_subgraph(self):

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
    
    self.directed_spanning_subgraph = {'directed_spanning_subgraphi_acyclic' : is_directed_acyclic_graph(self.directed_spanning_subgraph)}
    
    return self.directed_spanning_subgraph
#

