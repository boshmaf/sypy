from nose.tools import *
import sypy
import networkx as nx

class TestResults(object):
    """ Tests for BaseGraph class."""
    def setUp(self):
        sybil_region = sypy.Region(
            graph = sypy.CompleteGraph(num_nodes=10),
            name = "SybilCompleteGraph",
            is_sybil=True
        )

        honest_region = sypy.Region(
            graph = sypy.SmallWorldGraph(
                num_nodes=10,
                node_degree=2,
                rewire_prob=0.8
            ),
            name="HonestSmallWorldGraph"
        )

        honest_region.known_honests = [0]

        social_network = sypy.Network(
            left_region=honest_region,
            right_region=sybil_region,
            name="OnlineSocialNetwork"
        )
        social_network.random_pair_stitch(num_edges=2)

        detector = sypy.BaseDetector(social_network)
        self.known_honests = [0,1,2,3,4]
        detector.honests_predicted = self.known_honests

        self.results = sypy.Results(detector)


    def test_accuracy(self):
        eq_(self.results.accuracy(), 0.75)

    def test_sensitivity(self):
        eq_(self.results.sensitivity(), 1)

    def test_specificity(self):
        eq_(self.results.specificity(), 0.5)

    def test_cm(self):
        cm = self.results.confusion_matrix
        eq_(cm["N"], 10)
        eq_(cm["P"], 10)
        eq_(cm["FN"], 5)
        eq_(cm["TN"], 5)
        eq_(cm["FP"], 0)
        eq_(cm["TP"], 10)