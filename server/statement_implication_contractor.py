import networkx as nx
from lib.networkx.classes import digraph_extend
from lib.networkx.classes import dag

# SEE simple_cycles AND cycle_basis

def partition_cycle_clusters(cycle_nodes):
	"Given a bunch of nodes (that are ALL part of some cycle), return a set where each element is a single cycle"


def remove_sources_repeatedly(DG):
	while True:
		sources = DG.sources()
		# in future, this can be more efficient by looking at children of previous sources instead of finding the next level of sources from scratch
		if sources:
			DG.remove_nodes_from(sources)
		else:
			return DG


def find_dir_cycles(G):
	"Look for something like P0 --> P1 --> P2 --> P0 and return the guilty :) nodes"



	GC = G.clone()
	# delete all sources, since they can't be part of a cycle
	# delete all sinks, for the same reason
	# then same for sinks


	# repeat as long as you can!


	# what you are left with is cycle clusters
	set_of_cycle_clusters = partition_cycle_clusters(cycle_nodes)
	return set_of_cycle_clusters

def contract_dir_cycle():
	# or maybe just "contract nodes" can work in full generality
	"Combine the nodes into one"

