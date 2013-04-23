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


import sys
sys.path.append("../")

import sypy
import networkx as nx


if __name__ == "__main__":

    print "\n\nCustom graph..."
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from([0,1,2])
    nx_graph.add_edges_from([(0,1), (1,2), (2,0)])

    graph = sypy.CustomGraph(nx_graph)
    stats = graph.get_graph_stats()
    print "order={0}, size={1}, is_connected={2}".format(
        stats.order,
        stats.size,
        stats.is_connected
    )

    print "\n\nImported GEXF graph..."
    graph = sypy.ImportedGEXFGraph("datasets/ca-AstroPh.gexf")
    stats = graph.get_graph_stats()
    print "order={0}, size={1}, is_connected={2}, num_cc={3}".format(
        stats.order,
        stats.size,
        stats.is_connected,
        stats.num_cc
    )

    print "\nFiltering the graph (keeps LCC and non-outliers)"
    graph.lcc_degree_filter()
    stats = graph.get_graph_stats()
    print "order={0}, size={1}, is_connected={2}".format(
        stats.order,
        stats.size,
        stats.is_connected
    )

    print "\n\nPower-law graph with configurable average clustering"
    graph = sypy.PowerLawGraph(
        num_nodes=1000,
        node_degree=2,
        prob_triad=0.4
    )
    stats = graph.get_graph_stats()
    print "order={0}, size={1}, is_connected={2}".format(
        stats.order,
        stats.size,
        stats.is_connected
    )
    print "avg_clustering={0:.2f}, diameter={1}".format(
        stats.clustering_coefficient(),
        stats.diameter(),
    )
