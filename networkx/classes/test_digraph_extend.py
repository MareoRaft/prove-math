#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

#################################### MAIN #####################################
import networkx as nx
import digraph_extend

def test_is_nonnull(): # this is here really to make sure DiGraph inherited is_nonnull from Graph
	nn = nx.DiGraph()
	nn.add_node('a')
	assert nn.is_nonnull()

	nonnull = nx.DiGraph()
	nonnull.add_edge('s', 't')
	assert nonnull.is_nonnull()

	null = nx.DiGraph()
	assert null.is_nonnull() == False

def test_validate():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'b'],
		['c', 'd'],
	])
	assert DG.validate()

	try:
		DG.to_undirected().validate()
		assert False
	except AttributeError as e:
		assert str(e) == "'Graph' object has no attribute 'validate'"

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

def test_shortest_path(): # this tests the BUILT-IN function for DiGraphs, which finds the shortest DIRECTED path
	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', '1'], ['1', 'u'], ['u', '2'], ['2', 'd'],
		['b', 'm'],
		['c', 'm'],
	])
	assert DG.shortest_path('a', 'd') == ['a', '1', 'u', '2', 'd']
	assert DG.shortest_path('d', 'a') == None
	assert DG.shortest_path('c', 'b') == None
	assert DG.shortest_path({'a', 'b'}, {'c', 'd'}) == ['a', '1', 'u', '2', 'd']

def test_shortest_anydirectional_path():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.shortest_anydirectional_path('y', 'L') == ['y', 'c', 'L']
	assert DG.shortest_anydirectional_path('d', 't') == ['d', 'c', 't']
	assert DG.shortest_anydirectional_path('d', 'L') == ['d', 'c', 'L']
	assert DG.shortest_anydirectional_path('y', 't') == ['y', 'c', 't']

	# assert DG.shortest_anydirectional_path(['y', 'c'], ['L', 'd']) == (['c', 'L'] or ['c', 'd'])
	assert DG.shortest_anydirectional_path({'c', 'y'}, 'd') == ['c', 'd']

	DG.add_node('z')
	assert DG.shortest_anydirectional_path('z', 'c') == None

def test_ancestors():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.ancestors('t') == set() # b/c it typically returns a SET, it will return the empty set when there are no ancestors

def test_descendants():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.descendants('t') == {'c', 'L', 'd'}

def test_common_descendants():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.common_descendants('y', 't') == {'c', 'd', 'L'}
	assert DG.common_descendants('y', 'c') == {'d', 'L'}
	assert DG.common_descendants('d', 'd') == set()

	# assert DG.common_descendants({'y', 'c'}, 't') == {'d', 'L'}
	# assert DG.common_descendants('y', {'c', 't'}) == {'d', 'L'}

