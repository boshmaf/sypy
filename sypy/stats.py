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

import networkx as nx
import numpy as np
import math

class GraphStats():

    def __init__(self, graph):
        self.graph = graph

        self.order = self.graph.order()
        self.size = self.graph.size()

        self.cc = nx.connected_components(self.graph.structure)
        self.num_cc = len(self.cc)

        self.lcc = max(self.cc, key=len)
        self.lcc_order = len(self.lcc)
        self.lcc_size = len(
            self.graph.structure.edges(self.lcc)
        )

        self.scc = min(self.cc, key=len)
        self.scc_order = len(self.scc)
        self.scc_size = len(
            self.graph.structure.edges(self.scc)
        )

    def compute_mixing_time_bounds(self, variation_distance=None,
            variation_distance_scaler=1.0, lcc_only=False):
        """
        Returns the upper and the lower bounds for the mixing time of the
        graph parameterized by its variation distance. The approach computes
        the Second Largest Eigenvalue Modulus (SLEM) of the graph's transition
        matrix and calculates the bounds as described in Measuring the Mixing
        Time of Social Graphs, Mohaisen et al., IMC'10 (2010).
        """
        structure = self.graph.structure
        if self.num_cc != 1:
            if lcc_only:
                structure = self.graph.structure.subgraph(self.lcc)
            else:
                raise Exception("Graph is disconnected")

        if not variation_distance:
            variation_distance = variation_distance_scaler /\
                (float)(math.log10(structure.order()))

        if variation_distance < 0.0 or variation_distance > 1.0:
            raise Exception("Invalid variation distance value")

        adj_matrix = nx.to_numpy_matrix(structure)
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

        upper_bound = (math.log10(structure.order()) +\
            math.log10(1.0/(float)(variation_distance))) /\
                (float)(1.0 - second_largest)

        lower_bound = second_largest / (float)(2.0 * (1.0 - second_largest)) *\
                (math.log10(1.0 / (float)(2.0 * variation_distance)))

        return (lower_bound, upper_bound)

    def compute_cc_stats(self):
        """
        Returns basic statistics about the connected components of the
        graph. This includes their number, order, size, diameter, radius,
        average clusttering coefficient, transitivity, in addition to basic
        info about the largest and smallest connected components.
        """
        cc_stats = {}

        for index, component in enumerate(self.cc):
            cc_stats[index] = {}
            this_cc = cc_stats[index]

            this_cc["order"] = len(component)
            this_cc["size"] = len(
                self.graph.structure.edges(component)
            )

            subgraph = self.graph.structure.subgraph(component)
            this_cc["avg_cluster"] = nx.average_clustering(subgraph)
            this_cc["transitivity"] = nx.transitivity(subgraph)

            eccentricity = nx.eccentricity(subgraph)
            ecc_values = eccentricity.values()
            this_cc["diameter"] = max(ecc_values)
            this_cc["radius"] = min(ecc_values)

        return cc_stats
