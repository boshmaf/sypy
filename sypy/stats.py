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


class GraphStats():

    def __init__(self, graph, per_comp):
        self.graph = graph
        self.per_comp = per_comp

        self.order = self.graph.order()
        self.size = self.graph.size()
        self.cc_stats = self.__compute_cc_stats()

    def __compute_cc_stats(self):
        cc_stats = {}

        cc = nx.connected_components(self.graph.structure)
        cc_stats["num_cc"] = len(cc)

        lcc = max(cc, key=len)
        cc_stats["lcc_order"] = len(lcc)
        cc_stats["lcc_size"] = len(
            self.graph.structure.edges(lcc)
        )

        scc = min(cc, key=len)
        cc_stats["scc_order"] = len(scc)
        cc_stats["scc_size"] = len(
            self.graph.structure.edges(scc)
        )

        if self.per_comp:
            cc_stats["components"] = self.__compute_per_cc_stats(cc)

        return cc_stats

    def __compute_per_cc_stats(self, cc):
        cc_info = {}

        for index, component in enumerate(cc):
            cc_info[index] = {}
            this_cc = cc_info[index]

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

        return cc_info
