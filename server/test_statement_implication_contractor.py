########################## IMPORTS ##########################
import pytest
import networkx as nx

from statement_implication_contractor import *
from lib.node import create_appropriate_node


########################## HELPERS ##########################

########################### MAIN ###########################
def test_remove_sources_repeatedly():
	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	remove_sources_repeatedly(DG)
	assert not DG.nodes()

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	DG.add_path(['a', 'd', 'c'])
	remove_sources_repeatedly(DG)
	assert not DG.nodes()

	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b', 'c'])
	remove_sources_repeatedly(DG)
	assert len(DG.nodes()) == 3

	DG = nx.DiGraph()
	DG.add_edge('s', 'a')
	DG.add_cycle(['a', 'b', 'c', 'd'])
	DG.add_edge('d', 't')
	remove_sources_repeatedly(DG)
	assert DG.sources() == set()
	assert len(DG.nodes()) == 5

def test_remove_sinks_repeatedly():
	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	remove_sinks_repeatedly(DG)
	assert not DG.nodes()

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	DG.add_path(['a', 'd', 'c'])
	remove_sinks_repeatedly(DG)
	assert not DG.nodes()

	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b', 'c'])
	remove_sinks_repeatedly(DG)
	assert len(DG.nodes()) == 3

	DG = nx.DiGraph()
	DG.add_edge('s', 'a')
	DG.add_cycle(['a', 'b', 'c', 'd'])
	DG.add_edge('d', 't')
	remove_sinks_repeatedly(DG)
	assert DG.sinks() == set()
	assert len(DG.nodes()) == 5

def test_is_cycle_edge():
	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	assert not is_cycle_edge(DG, ('a', 'b'))

	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b', 'c'])
	assert is_cycle_edge(DG, ('a', 'b'))

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'a', 'e', 'f', 'g', 'h', 'f'])
	assert is_cycle_edge(DG, ('a', 'b'))
	assert not is_cycle_edge(DG, ('e', 'f'))
	assert is_cycle_edge(DG, ('f', 'g'))

def test_is_cycle_cluster_graph():
	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b', 'c'])
	assert is_cycle_cluster_graph(DG)

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	assert not is_cycle_cluster_graph(DG)

	DG = nx.DiGraph()
	DG.add_cycle(['a'])
	DG.add_edge('a', 'b')
	DG.add_cycle(['b'])
	assert not is_cycle_cluster_graph(DG)

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'a', 'e', 'f', 'g', 'h', 'f'])
	assert not is_cycle_cluster_graph(DG)

def test_partition_cycle_clusters():
	CG = nx.DiGraph()
	assert partition_cycle_clusters(CG) == set()

	CG = nx.DiGraph()
	CG.add_cycle(['a', 'b', 'c'])
	assert partition_cycle_clusters(CG) == {frozenset({'a', 'b', 'c'})}

	CG = nx.DiGraph()
	CG.add_cycle(['a', 'b', 'c', 'd'])
	CG.add_cycle(['a', 'b', 't', 'm'])
	assert partition_cycle_clusters(CG) == {frozenset({'a', 'b', 'c', 'd', 't', 'm'})}

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'a', 't', 'a'])
	DG.add_path(['x', 'y', 'z', 'x'])
	assert partition_cycle_clusters(DG) == {
		frozenset({'a', 'b', 'c', 't'}),
		frozenset({'x', 'y', 'z'}),
	}





