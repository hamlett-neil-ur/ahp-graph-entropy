#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:00:34 2026

@author: nahamlet
"""

from itertools import product
from pandas import DataFrame, concat

evidentiary_span = (set(hi_mod.comparative_judgements['reference_factor'])
                         .union(hi_mod.comparative_judgements['comparative_factor']))

pairwise_span = (DataFrame(data = product(evidentiary_span,
                                          repeat = 2       ),
                          columns = ['reference_factor',
                                     'comparative_factor'])   )


reciprocal_matrix_off_diagonals = concat(objs = [pairwise_span
                                                   .merge(right = hi_mod.comparative_judgements),
                                                 pairwise_span
                                                   .merge(right = hi_mod.comparative_judgements
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

hi_mod.reciprocal_matrix = reciprocal_matrix