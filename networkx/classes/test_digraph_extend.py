import networkx as nx
import graph_extend
import digraph_extend

def test_validate():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'b'],
		['c', 'd'],
	])
	assert DG.validate()

	# assert undirected.validate()

def test_predecessor():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.predecessor('c') in {'y', 't'}

def test_successor():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.successor('c') in {'d', 'L'}

def test_is_source():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.is_source('y')
	assert DG.is_source('t')
	assert DG.is_source('c') == False
	assert DG.is_source('d') == False

def test_shortest_anydirectional_path():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.shortest_anydirectional_path('y', 'L') == ['y', 'c', 'L']


