################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import graph_extend

#################################### MAIN #####################################
def test_is_nonnull():
	nonnull = nx.Graph()
	nonnull.add_node('a')
	assert nonnull.is_nonnull()

	nonnull = nx.Graph()
	nonnull.add_edge('s', 't')
	assert nonnull.is_nonnull()

	null = nx.Graph()
	assert null.is_nonnull() == False

def test_is_null():
	nonnull = nx.Graph()
	nonnull.add_node('a')
	assert nonnull.is_null() == False

	nonnull = nx.Graph()
	nonnull.add_edge('s', 't')
	assert nonnull.is_null() == False

	null = nx.Graph()
	assert null.is_null()

def test_add_node_unique():
	G = nx.Graph()
	for i in range(0, 1000):
		G.add_node_unique()
	assert len(G.nodes()) == 1000


