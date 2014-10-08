# What is SyPy?

SyPy is an easy-to-use Python package for [Sybil node](http://dl.acm.org/citation.cfm?id=687813) detection in social and information networks. Such networks are modelled as [graphs](http://en.wikipedia.org/wiki/Graph_(mathematics)), where a node represents an entity and an edge between two nodes represents a connection. For example, in online social networks such as Facebook, nodes represent users and edges represent social relationships like friendships.

In the Sybil attack, an adversary controls a set of nodes in the network and uses them for adversarial objectives. For example, [socialbots](http://lersse-dl.ece.ubc.ca/record/277) in online social networks are automation tools that control hijacked or adversary-owned user accounts, which are adversely used to infiltrate these networks, steal user data, spread misinformation, or distribute malware.

SyPy specializes in evaluating the [effectiveness](http://en.wikipedia.org/wiki/Binary_classification) of graph-based Sybil node detection algorithms on a reasonable scale (i.e., networks consisting of thousands of nodes). It is not designed to benchmark the effeciency of these algorithms on a large scale, which is a rather interesting but orthogonal topic. When detecting Sybils using graphs, there are three [assumptions](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6151333) made about the network:

1. The defender knows at least one honest (i.e., non-Sybil) node.
2. The network structure (i.e., its graph) has two regions (sub-graphs): the honest region consisting of honest nodes, and the Sybil region consisting of Sybil nodes. These two regions represent disjoint [communities](http://www.sciencedirect.com/science/article/pii/S0370157309002841) or [clusters](http://www.sciencedirect.com/science/article/pii/S1574013707000020), meaning they are "loosely connected" together as compared to their own proportionally more connected structures.
3. The honest region is [fast mixing](http://dl.acm.org/citation.cfm?id=1879191), meaning it is "well connected."

Given that all of the assumptions above hold, most of the well-known detection algorithms try in one way or the other to cut the network into two [partitions](http://en.wikipedia.org/wiki/Graph_partition) such that the cut size is small or sparse. After that, the partition to which the known honest node belongs is declared as the honest region (and the other as Sybil).

# How does it work?

SyPy provides a simple framework to design, implement, and evaluate graph-based Sybil detection algorithms. Overall, there are four main abstractions: graphs, regions, networks, and detection algorithms.

## Graphs and Regions

A region is either Sybil or honest, and it has a specific graph structure. For example, you can create a Sybil region of 100 nodes that are fully-connected (i.e., a [complete graph](http://en.wikipedia.org/wiki/Complete_graph)) as follows:

    import sypy

    sybil_region = sypy.Region(
        graph=sypy.CompleteGraph(num_nodes=100),
        name="SybilCompleteGraph", 
        is_sybil=True
    )

SyPy supports many [random graph](http://en.wikipedia.org/wiki/Random_graph) models such as [scale-free](http://en.wikipedia.org/wiki/Scale-free_network) and [small-world](http://en.wikipedia.org/wiki/Small_world_network) graphs or network structures. For example, you can create an honest region that represents a real-world social network consisting of 5000 users, and then pick 10 random nodes to be known honest nodes as follows:

    honest_region = sypy.Region(
        graph=sypy.SmallWorldGraph(
            num_nodes=5000,
            node_degree=100,
            rewiring_prob=0.8
        ),
        name="HonestSmallWorldGraph"
    )
    honest_region.pick_random_honest_nodes(num_nodes=10)

## Networks

A network always consists of two regions: the honest region positioned to the left, and the Sybil region positioned to the right. The regions can have any graph structure, and initially, they are disconnected. We can "stitch" the two regions together in many ways that resemble how Sybils connect with honest nodes in real-world networks (i.e., using a random or targeted adversarial infiltration strategy). For example, using the regions defined above, we can create a network and connect ten randomly-picked pair, one node from both region, as follows:

    social_network = sypy.Network(
        left_region=honest_region,
        right_region=sybil_region,
        name="OnlineSocialNetwork"
    )
    social_network.random_pair_stitch(num_edges=10)

## Detectors

After the network is updated, we can run any of the supported [graph-based Sybil detection algorithms](http://dl.acm.org/citation.cfm?doid=2034575.2034593) and compute their detection performance. For example, we can use [SybilGuard](http://dl.acm.org/citation.cfm?id=1159945), one of the first graph-based Sybil detection algorithms with provable guarantees, as follows:

    detector = sypy.SybilGuardDetector(social_network)
    results = detector.detect()

    print "accuracy={0:.2f}, sensitivity={1:.2f}, specificity={2:.2f}".format(
        results.accuracy(),
        results.sensitivity(),
        results.specificity()
    )

# How extensible is it?

SyPy is built on top of [NetworkX](http://networkx.lanl.gov/), and hence it can support most of NetworkX functionality, which also means it is easily extensible. For example, you can visualize any region or network as follows:

    sybil_region.visualize()
    sybil_region.visualize(file_path="/tmp/{0}".format(sybil_region.name))

    network.visualize()
    network.visualize(file_path="/tmp/{0}".format(network.name))

# Who is working on it?

SyPy started as a research project at the [University of British Columbia](http://www.ece.ubc.ca/) (UBC) by [Yazan Boshmaf](http://ece.ubc.ca/~boshmaf). Latere on, the following people contributed in one way or the other:

* Tony Cheng (UBC) -- Region and network visualization.

# Reference

If you used SyPy in your work and found it useful, please reference it as follows:

> Yazan Boshmaf, Konstantin Beznosov, Matei Ripeanu. *"Graph-based Sybil detection is social and information systems"*. In Proceedings of the 2013 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM'13), Niagara Falls, Canada, August 25-28, 2013.
