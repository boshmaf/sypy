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


if __name__ == "__main__":

    sybil_region = sypy.Region(
        graph = sypy.CompleteGraph(num_nodes=10000),
        name = "SybilCompleteGraph",
        is_sybil=True
    )


    gexf_graph = sypy.ImportedGEXFGraph("datasets/ca-HepTh.gexf")
    gexf_graph.lcc_degree_filter()
    honest_region = sypy.Region(
        graph=gexf_graph,
        name="HonestRealWorldGraph"
    )
    honest_region.pick_random_honest_nodes(num_nodes=10)

    social_network = sypy.Network(
        left_region=honest_region,
        right_region=sybil_region,
        name="OnlineSocialNetwork"
    )
    social_network.random_pair_stitch(num_edges=10)

    detector = sypy.SybilRankDetector(social_network)
    results = detector.detect()
    print "Detection performance:"
    print "accuracy={0:.2f}, sensitivity={1:.2f}, specificity={2:.2f}".format(
        results.accuracy(),
        results.sensitivity(),
        results.specificity()
    )

    answer = raw_input("Visualize [y/n]: ")
    if answer == "y":
        print "This will take sometime..."
        social_network.visualize()
