#    SyPy: A Python framework for evaluating graph-based Sybil detection
#    algorithms in social and information networks.
#    
#    Copyright (C) 2013  Yazan Boshmaf
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import graphs as sypy_graphs
import networkx as nx
import numpy as np
import math

def compute_mixing_time_bounds(graph, variation_distance=None,
    variation_distance_scaler=1.0
):
    """
    Returns the upper and the lower bounds for the mixing time of the graph
    parameterized by its variation distance. The approach computes the
    Second Largest Eigenvalue Modulus (SLEM) of the graph's transition matrix
    and calculates the bounds as described in Measuring the Mixing Time of
    Social Graphs, Mohaisen et al., IMC'10 (2010).
    """
    if not isinstance(graph, sypy_graphs.BasicGraph):
        raise Exception("Invalid graph")

    if not variation_distance:
        variation_distance = variation_distance_scaler / (float)(math.log10(graph.order()))

    if variation_distance < 0.0 or variation_distance > 1.0:
        raise Exception("Invalid variation distance value")

    adj_matrix = nx.to_numpy_matrix(graph.structure)
    matrix_dim = adj_matrix.shape

    trans_matrix = np.empty(matrix_dim)
    for row in xrange(matrix_dim[0]):
        for col in xrange(matrix_dim[1]):
            node_degree = adj_matrix[row].sum()
            if node_degree == 0:
                raise Exception("The graph has disconnected components")
            if adj_matrix[row, col] == 0.0:
                trans_matrix[row, col] = 0.0
            else:
                trans_matrix[row,col] = 1/node_degree

    eigen_vals = np.linalg.eig(trans_matrix)[0]
    second_largest = math.fabs(np.sort(eigen_vals)[-2])

    upper_bound = (math.log10(graph.structure.order()) +\
        math.log10(1.0/(float)(variation_distance))) /\
            (float)(1.0 - second_largest)

    lower_bound = second_largest / (float)(2.0 * (1.0 - second_largest)) *\
        (math.log10(1.0 / (float)(2.0 * variation_distance)))

    return (lower_bound, upper_bound)
