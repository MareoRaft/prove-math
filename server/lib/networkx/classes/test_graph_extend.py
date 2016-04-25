############################ IMPORTS ##############################
import networkx as nx
import pytest

from lib.networkx.classes import graph_extend

############################## MAIN ###############################
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

def test_acceptable_iterable():
	G = nx.Graph()
	assert G.acceptable_iterable('single_node') == False
	assert G.acceptable_iterable(['this', 'is', 'a', 'list']) == True
	assert G.acceptable_iterable({'this', 'is', 'a', 'set'}) == True
	assert G.acceptable_iterable({'test': 'dict'}) == False
	assert G.acceptable_iterable(1) == False

def test_validate_input_nodes():
	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])

	#testing nonexistent inputs:
	with pytest.raises(nx.NetworkXError):
		DG.validate_input_nodes('NotANode')
	with pytest.raises(nx.NetworkXError):
		DG.validate_input_nodes(['NotANode'])
	with pytest.raises(nx.NetworkXError):
		DG.validate_input_nodes(['x', 'NotANode', 'z'])
	with pytest.raises(ValueError):
		DG.validate_input_nodes([])

	#existing inputs:
	assert DG.validate_input_nodes('x')
	assert DG.validate_input_nodes(['x', 'y'])

