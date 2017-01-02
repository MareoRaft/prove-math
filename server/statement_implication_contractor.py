import networkx as nx
from lib.networkx.classes import digraph_extend
from lib.networkx.classes import dag

def remove_sources_repeatedly(DG):
	while True:
		sources = DG.sources()
		# in future, this can be more efficient by looking at children of previous sources instead of finding the next level of sources from scratch
		if sources:
			DG.remove_nodes_from(sources)
		else:
			return DG

def remove_sinks_repeatedly(DG):
	while True:
		sinks = DG.sinks()
		if sinks:
			DG.remove_nodes_from(sinks)
		else:
			return DG

# SEE simple_cycles AND cycle_basis AND find_cycle for three useful BUILTIN methods!

def is_cycle_edge(DG, edge):
	ancestor_nodes = DG.ancestors(edge[0])
	return edge[1] in ancestor_nodes

def is_cycle_cluster_graph(DG):
	if DG.sources():
		return False
	if DG.sinks():
		return False
	for edge in DG.edges():
		if not is_cycle_edge(DG, edge):
			return False
	return True

def partition_cycle_clusters(CG):
	"Given a graph that consists of cycle clusters only, return a set where each element is a single cycle cluster"
	if not is_cycle_cluster_graph(CG):
		raise ValueError('The input graph cannot have any sources, sinks, or any edges that are not part of a cycle.')
	cycle_clusters = set()
	while CG.nodes():
		node = CG.nodes()[0]
		cycle_cluster = CG.ancestors(node)
		cycle_cluster.add(node) # don't forget node!
		CG.remove_nodes_from(cycle_cluster)
		cycle_clusters.add(frozenset(cycle_cluster))
	return cycle_clusters

def find_dir_cycles(G):
	"Look for something like P0 --> P1 --> P2 --> P0 and return the guilty :) nodes"
	GC = G.clone()
	# delete all sources, since they can't be part of a cycle
	remove_sources_repeatedly(GC)
	# delete all sinks, for the same reason
	remove_sinks_repeatedly(GC)

	# what you are left with is cycle clusters
	cycle_clusters = partition_cycle_clusters(GC, cycle_nodes)
	return cycle_clusters

def contract_dir_cycle():
	# or maybe just "contract nodes" can work in full generality
	"Combine the nodes into one"

