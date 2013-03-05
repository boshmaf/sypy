from nose.tools import *
import sypy
import networkx as nx


class TestBaseGraph(object):
    def setUp(self):
        graph = nx.Graph()
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(0,2)
        self.graph = sypy.BaseGraph()
        self.graph.structure = graph
        self.stats = sypy.Stats(self.graph)

    def test(self):
        eq_(self.graph.order(), 3)
        eq_(self.graph.nodes(), [0,1,2])
        for edge in [(0,1), (1,2), (0,2)]:
            ok_(edge in self.graph.edges())
        eq_(self.graph.size(), 3)
        eq_(self.stats, self.graph.get_graph_stats())