from nose.tools import *
import sypy
import networkx as nx
import os


class TestBaseGraph(object):
    """ Tests for BaseGraph class."""
    def setUp(self):
        self.tri_nx_graph = nx.complete_graph(3)
        self.tri_nx_graph[0][1]["weight"] = 0.9
        self.tri_nx_graph[1][2]["weight"] = 2.1
        self.tri_nx_graph[0][2]["weight"] = -.5
        self.tri_graph = sypy.BaseGraph()
        self.tri_graph.structure = self.tri_nx_graph

    def test_order(self):
        eq_(self.tri_graph.order(), self.tri_nx_graph.order())

    def test_edges(self):
        eq_(self.tri_graph.edges(), self.tri_nx_graph.edges())
        eq_(self.tri_graph.edges(True), self.tri_nx_graph.edges(data=True))

    def test_nodes(self):
        eq_(self.tri_graph.nodes(), self.tri_nx_graph.nodes())
        eq_(self.tri_graph.nodes(True), self.tri_nx_graph.nodes(data=True))

    def test_size(self):
        eq_(self.tri_graph.size(), self.tri_nx_graph.size())
        eq_(self.tri_graph.size("weight"), self.tri_nx_graph.size(weight="weight"))

    def test_stats(self):
        self.stats = sypy.Stats(self.tri_graph)
        eq_(self.stats.__dict__, self.tri_graph.get_graph_stats().__dict__)

    def test_export_gexf(self):
        self.tri_graph.export_to_gexf_file("gexf_test", compressed=True)
        self.tri_graph.export_to_gexf_file("gexf_test", compressed=False)

        os.remove("gexf_test")
        os.remove("gexf_test.gz")


class TestCustomGraph(object):
    """ Tests for CustomGraph class."""
    def setUp(self):
        self.nx_graph = nx.complete_graph(5)
        self.tri_graph = sypy.CustomGraph(self.nx_graph)

    def test_structure(self):
        eq_(self.tri_graph.structure, self.nx_graph)

class TestImportedGEXFGraph(object):
    """ Tests for ImportedGEXFGraph class."""
    def setUp(self):
        complete_graph = sypy.BaseGraph()
        complete_graph.export_to_gexf_file("gexf_test", compressed=True)
        complete_graph.export_to_gexf_file("gexf_test", compressed=False)

        self.compressed_gexf_graph = sypy.ImportedGEXFGraph("gexf_test.gz")
        self.uncompressed_gexf_graph = sypy.ImportedGEXFGraph('gexf_test')

    def tearDown(self):
        os.remove("gexf_test")
        os.remove("gexf_test.gz")

    @raises(Exception)
    def test_wrong_graph(self):
        digraph = sypy.CustomGraph(nx.DiGraph())
        digraph.export_to_gexf_file("DiGraph", compressed=True)
        try:
            digraph = sypy.ImportedGEXFGraph("DiGraph")
        except Exception:
            os.remove("DiGraph.gz")
            return
        finally:
            os.remove("DiGraph.gz")
            ok_(false)

class TestZacharyKarateClubGraph(object):
    """ Tests for ZacharyKarateClubGraph class."""
    def setUp(self):
        self.karate_club = sypy.ZacharyKarateClubGraph()

    def test_type(self):
        eq_(type(self.karate_club.structure), type(nx.karate_club_graph()))

class TestFlorentineFamiliesGraph(object):
    """ Tests for FlorentineFamiliesGraph class."""
    def setUp(self):
        self.florentine_families_graph = sypy.FlorentineFamiliesGraph()

    def test_type(self):
        eq_(type(self.florentine_families_graph.structure), type(nx.florentine_families_graph()))

class TestCompleteGraph(object):
    """ Tests for CompleteGraph class."""
    def setUp(self):
        self.num_nodes = 10
        self.complete_graph = sypy.CompleteGraph(self.num_nodes)

    def test_size(self):
        expected_size = self.num_nodes * (self.num_nodes - 1) / 2
        eq_(self.complete_graph.size(), expected_size)

class TestSmallWorldGraph(object):
    """ Tests for SmallWorldGraph class."""
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
    """ Tests for PowerLawGraph class."""
    def setUp(self):
        self.num_nodes = 10
        self.node_degree = 2
        self.prob_triad = 0.5
        self.seed = None
        self.powerlaw_graph = sypy.PowerLawGraph(
            self.num_nodes,
            self.node_degree,
            self.prob_triad,
            self.seed
        )

    def test_consistecy(self):
        eq_(self.num_nodes, self.powerlaw_graph.num_nodes)
        eq_(self.node_degree, self.powerlaw_graph.node_degree)
        eq_(self.prob_triad, self.powerlaw_graph.prob_triad)
        eq_(self.seed, self.powerlaw_graph.seed)

    def test_connected(self):
        ok_(nx.is_connected(self.powerlaw_graph.structure))

class TestGirvanNewmanCommunityGraph(object):
    """ Tests for GirvanNewmanCommunityGraph class."""
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

    def test_order(self):
        expected_order = self.num_comm * self.comm_size
        eq_(expected_order, self.girvan_newman_graph.order())

    def test_size(self):
        ok_(self.girvan_newman_graph.size() > 0)

    def smoke_test(self):
        self.null_comm_size = sypy.GirvanNewmanCommunityGraph(comm_size=0)
        self.single_comm = sypy.GirvanNewmanCommunityGraph(num_comm=1)
        self.null_comm = sypy.GirvanNewmanCommunityGraph(num_comm=0)

    def negative_values(self):
        self.neg_comm_size = sypy.GirvanNewmanCommunityGraph(comm_size=-5)
        self.neg_comm_num = sypy.GirvanNewmanCommunityGraph(num_comm=-5)


class TestLFRCommunityGraph(object):
    """ Tests for TestLFRCommunityGraph class."""
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
