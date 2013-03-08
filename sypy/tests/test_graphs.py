from nose.tools import *
import sypy
import networkx as nx


class TestBaseGraph(object):
    def setUp(self):
        self.edge_list = [(0,1), (1,2), (0,2)]
        self.node_list = [0,1,2]
        self.num_nodes = 3
        self.tri_graph = sypy.BaseGraph()
        self.tri_graph.structure.add_edges_from(self.edge_list)

        self.weighted_graph = sypy.BaseGraph()
        self.weighted_graph.structure.add_edge(0,1,weight=0.9)
        self.weighted_graph.structure.add_edge(1,2,weight=2.1)
        self.weighted_graph.structure.add_edge(0,2,weight=-.5)

        self.colored_graph = sypy.BaseGraph()
        self.colored_graph.structure.add_node(0, {'color':'red'})
        self.colored_graph.structure.add_node(1, {'color':'yellow'})
        self.colored_graph.structure.add_node(2, {'color':'green'})

    def test_order(self):
        eq_(self.tri_graph.order(), self.num_nodes)
        self.tri_graph.structure.remove_node(2)
        eq_(self.tri_graph.order(), self.num_nodes-1)

    def test_edges(self):
        for edge in self.edge_list:
            ok_(edge in self.tri_graph.edges())
        self.tri_graph.structure.add_edge(3,4)
        for edge in self.edge_list+[(3,4)]:
            ok_(edge in self.tri_graph.edges())

    def test_edges_data(self):
        ok_('weight' in str(self.weighted_graph.edges(True)))
        ok_('weight' not in str(self.tri_graph.edges(True)))
        ok_('weight' not in str(self.colored_graph.edges(True)))

    def test_nodes(self):
        eq_(self.tri_graph.nodes(), self.node_list)
        self.tri_graph.structure.add_node(3)
        eq_(self.tri_graph.nodes(), self.node_list+[3])

    def test_nodes_data(self):
        ok_('color' in str(self.colored_graph.nodes(True)))
        ok_('color' not in str(self.weighted_graph.nodes(True)))
        ok_('color' not in str(self.tri_graph.nodes(True)))

    def test_size(self):
        eq_(self.tri_graph.size(), 3)
        self.tri_graph.structure.add_edge(2,3)
        eq_(self.tri_graph.size(), 4)
        self.tri_graph.structure.remove_edge(0,1)
        eq_(self.tri_graph.size(), 3)

    def test_weight(self):
        eq_(self.weighted_graph.size('weight'), 2.5)
        self.weighted_graph.structure.add_edge(2,3,weight=-3)
        eq_(self.weighted_graph.size('weight'), -0.5)

    def test_stats(self):
        self.stats = sypy.Stats(self.tri_graph)
        eq_(self.stats.__dict__, self.tri_graph.get_graph_stats().__dict__)

    def test_type(self):
        eq_(type(self.tri_graph.structure), type(nx.Graph()))
        eq_(type(self.weighted_graph.structure), type(nx.Graph()))


class TestCustomGraph(object):
    def setUp(self):
        self.nx_graph = nx.Graph()
        self.nx_graph.add_nodes_from(range(10))
        self.tri_graph = sypy.CustomGraph(self.nx_graph)

    def test_dict(self):
        eq_(self.nx_graph.__dict__, self.tri_graph.structure.__dict__)
        self.nx_graph = nx.DiGraph()
        self.nx_graph.add_nodes_from(range(10))
        ok_(self.nx_graph.__dict__ != self.tri_graph.structure.__dict__)

    def test_type(self):
        eq_(type(self.nx_graph), type(self.tri_graph.structure))
        self.nx_graph = nx.DiGraph()
        self.nx_graph.add_nodes_from(range(10))
        ok_(type(self.nx_graph) != type(self.tri_graph.structure))

class TestImportedGEXFGraph(object):
    def setUp(self):
        self.compressed_gexf_graph = sypy.ImportedGEXFGraph('gexf_test.gz')
        self.uncompressed_gexf_graph = sypy.ImportedGEXFGraph('gexf_test')

    def test_nodes(self):
        eq_(self.compressed_gexf_graph.nodes(), range(10))
        eq_(self.uncompressed_gexf_graph.nodes(), range(10))

class TestZacharyKarateClubGraph(object):
    def setUp(self):
        self.karate_club = sypy.ZacharyKarateClubGraph()

    def test_type(self):
        eq_(type(self.karate_club.structure), type(nx.karate_club_graph()))

class TestFlorentineFamiliesGraph(object):
    def setUp(self):
        self.florentine_families_graph = sypy.FlorentineFamiliesGraph()

    def test_type(self):
        eq_(type(self.florentine_families_graph.structure), type(nx.florentine_families_graph()))

class TestCompleteGraph(object):
    def setUp(self):
        self.num_nodes = 10
        self.complete_graph = sypy.CompleteGraph(self.num_nodes)

    def test_order(self):
        eq_(self.num_nodes, self.complete_graph.order())
        self.complete_graph.add_node(10)
        eq_(self.num_nodes+1, self.complete_graph.order())

    def test_type(self):
        eq_(type(self.complete_graph.structure), type(nx.complete_graph(self.num_nodes)))

    def test_size(self):
        expected_size = self.num_nodes * (self.num_nodes - 1) / 2
        eq_(self.complete_graph.size(), expected_size)

class TestSmallWorldGraph(object):
    def setUp(self):
        self.num_nodes = 10
        self.node_degree = 2
        self.rewire_prob = 0.5
        self.tries = 2
        self.seed = 9999
        self.small_world_graph = sypy.SmallWorldGraph(
            self.num_nodes,
            self.node_degree,
            self.rewire_prob,
            self.tries,
            self.seed
        )

    def test_consistency(self):
        eq_(self.num_nodes, self.small_world_graph.num_nodes)
        eq_(self.node_degree, self.small_world_graph.node_degree)
        eq_(self.rewire_prob, self.small_world_graph.rewire_prob)
        eq_(self.tries, self.small_world_graph.tries)
        eq_(self.seed, self.small_world_graph.seed)


class TestPowerLawGraph(object):
    def setUp(self):
        self.num_nodes = 10
        self.node_degree = 2
        self.prob_triad = 0.5
        self.seed = 9999
        self.powerlaw_graph = sypy.PowerLawGraph(
            self.num_nodes,
            self.node_degree,
            self.prob_triad,
            self.seed
        )
        self.nx_graph = nx.powerlaw_cluster_graph(
            self.num_nodes,
            self.node_degree,
            self.prob_triad,
            self.seed
        )

    def test_dict(self):
        eq_(self.powerlaw_graph.structure.__dict__, self.nx_graph.__dict__)

    def test_consistecy(self):
        eq_(self.num_nodes, self.powerlaw_graph.num_nodes)
        eq_(self.node_degree, self.powerlaw_graph.node_degree)
        eq_(self.prob_triad, self.powerlaw_graph.prob_triad)
        eq_(self.seed, self.powerlaw_graph.seed)

    def test_type(self):
        eq_(type(self.powerlaw_graph.structure), type(nx.powerlaw_cluster_graph(10, 2, 0.5)))

    def test_connected(self):
        ok_(nx.is_connected(self.powerlaw_graph.structure))

class TestGirvanNewmanCommunityGraph(object):
    def setUp(self):
        self.num_comm = 4
        self.comm_size = 32
        self.avg_intercomm = 1
        self.seed = None
        self.girvan_newman_graph = sypy.GirvanNewmanCommunityGraph(
            self.num_comm,
            self.comm_size,
            self.avg_intercomm,
            self.seed
        )

    def test_consistency(self):
        eq_(self.num_comm, self.girvan_newman_graph.num_comm)
        eq_(self.comm_size, self.girvan_newman_graph.comm_size)
        eq_(self.avg_intercomm, self.girvan_newman_graph.avg_intercomm)
        eq_(self.seed, self.girvan_newman_graph.seed)

    def test_order(self):
        expected_order = self.num_comm * self.comm_size
        eq_(expected_order, self.girvan_newman_graph.order())

    def test_size(self):
        ok_(self.girvan_newman_graph.size() > 0)

class TestLFRCommunityGraph(object):
    def setUp(self):
        self.num_comm = 3
        self.max_comm = 100
        self.comm_exp = 1.5
        self.max_degree = 10
        self.degree_exp = 1.5
        self.mixing_par = 0.075
        self.tries = 3
        self.seed = 1234
        self.lfr_graph = sypy.LFRCommunityGraph(
            self.num_comm,
            self.max_comm,
            self.comm_exp,
            self.max_degree,
            self.degree_exp,
            self.mixing_par,
            self.tries,
            self.seed
        )

    def test_consistency(self):
        eq_(self.num_comm, self.lfr_graph.num_comm)
        eq_(self.max_comm, self.lfr_graph.max_comm)
        eq_(self.comm_exp, self.lfr_graph.comm_exp)
        eq_(self.max_degree, self.lfr_graph.max_degree)
        eq_(self.degree_exp, self.lfr_graph.degree_exp)
        eq_(self.mixing_par, self.lfr_graph.mixing_par)
        eq_(self.tries, self.lfr_graph.tries)
        eq_(self.seed, self.lfr_graph.seed)

    def test_order(self):
        ok_(self.lfr_graph.order() > 0)

    def test_size(self):
        ok_(self.lfr_graph.size() > 0)
