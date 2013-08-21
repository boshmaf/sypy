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
        graph = sypy.PowerLawGraph(
            num_nodes=1000,
            node_degree=4,
            prob_triad=0.75
        ),
        name = "SybilCompleteGraph",
        is_sybil=True
    )
    sybil_stats = sybil_region.get_region_stats()
    assert sybil_stats.is_connected == True

    honest_region = sypy.Region(
        graph=sypy.PowerLawGraph(
            num_nodes=1000,
            node_degree=4,
            prob_triad=0.75
        ),
        name="HonestPowerLawGraph"
    )
    honest_region.pick_random_honest_nodes(num_nodes=10)
    honest_stats = honest_region.get_region_stats()
    assert honest_stats.is_connected == True

    social_network = sypy.Network(
        left_region=honest_region,
        right_region=sybil_region,
        name="OnlineSocialNetwork"
    )
    social_network.random_pair_stitch(num_edges=10)

    roc_benchmark = sypy.RocAnalysisBenchmark(
        detector=sypy.SybilPredictDetector(social_network),
        threshold="pivot",
    )
    roc_benchmark.run()
    roc_benchmark.plot(file_name="roc_curve")
    
    auc = roc_benchmark.roc_curve["auc"]
    print "Benchmark results: AUC={0:.2f}".format(auc)

    answer = raw_input("Visualize [y/n]: ")
    if answer == "y":
        print "This will take some time..."
        social_network.visualize()
