################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import digraph_extend
#for test_most_important:
#from lib.networkx.classes import dag
from lib.node import create_appropriate_node, Node

#################################### MAIN #####################################
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

def test_hanging_dominion():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.hanging_dominion(['y']) == set('c')
	assert DG.hanging_dominion(['y', 't']) == set('c')
	assert DG.hanging_dominion(['c']) == {'L', 'd'}
	assert DG.hanging_dominion(['y', 'c']) == {'L', 'd'}

def test_absolute_dominion():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.absolute_dominion(['y']) == ['y']
	assert set(DG.absolute_dominion(['y', 't'])) == {'c', 'y', 't'}
	assert set(DG.absolute_dominion(['y', 'c'])) == {'L', 'd', 'y', 'c'}

	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'b'], ['b', 'c'],
		['x', 'c'],
	])
	assert set(DG.absolute_dominion(['a', 'x'])) == {'b', 'a', 'x'}

def test_single_source_shortest_anydirectional_path_length():
	G = nx.DiGraph()
	G.add_path([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
	x = G.single_source_shortest_anydirectional_path_length(5, 3)
	assert len(x) == 7
	assert x == {3: 2, 4: 1, 5: 0, 6: 1, 7: 2, 8: 3, 2: 3}

def test_multiple_sources_shortest_path_length():
	G = nx.DiGraph()
	G.add_path([0, 1, 2, 3, 4, 5, 6])
	d = G.multiple_sources_shortest_path_length([3], 2)
	assert d == {3:0, 4:1, 5:2}

	G = nx.DiGraph()
	G.add_path([0, 1, 2, 3, 4, 5, 6])
	d = G.multiple_sources_shortest_path_length([3, 4], 2)
	assert d == {3:0, 4:0, 5:1, 6:2}

	G = nx.DiGraph()
	G.add_path(['a', 'y', 'd'])
	G.add_path(['a', 'l', 'x'])
	G.add_path(['a', 'c'])
	G.add_path(['b', 'c'])
	G.add_path(['b', 'd', 'l'])
	G.add_path(['b', 't', 'x'])
	d = G.multiple_sources_shortest_path_length(['a', 'b'])
	assert d == {
		'a': 0, 'b': 0,
		'c': 1, 'y': 1, 'd': 1, 'l': 1, 't': 1,
		'x': 2,
	}

def test_common_ancestors():
	#remember to try other edge cases
	#possibly reimplement for better efficiency
	DG = nx.DiGraph()
	DG.add_path(['a', 'x'])
	DG.add_path(['b', 'y'])
	d = DG.common_ancestors('x', 'y')
	assert d == set([])
	
	DG = nx.DiGraph()
	DG.add_path(['a', 'x'])
	DG.add_node('y')
	d = DG.common_ancestors('x', 'y')
	assert d == set([])
	
	DG = nx.DiGraph()
	DG.add_node('x')
	DG.add_node('y')
	d = DG.common_ancestors('x', 'y')
	assert d == set([])
	
	DG = nx.DiGraph()
	DG.add_path(['a', 'x'])
	DG.add_path(['b', 'x'])
	DG.add_path(['b', 'y'])
	DG.add_path(['c', 'y'])
	d = DG.common_ancestors('x', 'y')
	assert d == set(['b']) #{'b'} but using {} for empty set will give a dict, use set() instead
	
	DG = nx.DiGraph()
	DG.add_path(['a', 'x'])
	DG.add_path(['b', 'x'])
	DG.add_path(['b', 'y'])
	DG.add_path(['c', 'y'])
	DG.add_path(['d', 'b'])
	d = DG.common_ancestors('x', 'y')
	assert d == set(['b','d'])
	
	#test empty set as an arg
	#test sets of nodes as args
	#test node that doesn't exist as arg

def test_most_important():
#prenodes need "type","def","description","name","importance"
	pre_a = {"type":"theorem","description":"This is node aaaaaaaaaa","name":"K","importance":2}
	# a = create_appropriate_node(pre_a)
	a = Node(pre_a)
	# pre_b = {"type":"def","content":"This is node b","importance":5}
	# b = create_appropriate_node(pre_b)
	# pre_c = {"type":"def","content":"This is node c","importance":8}
	# c = create_appropriate_node(pre_c)
	# pre_d = {"type":"def","content":"This is node d","importance":8}
	# d = create_appropriate_node(pre_d)
	# 
	DG = nx.DiGraph()
	DG.add_n(a)
#	assert DG.most
	# DG.add_n(b)
	# DG.add_n(c)
	# DG.add_n(d)
# 

def test_unlearned_dependency_tree():
	DG = nx.DiGraph()

	#need to fix this one!
#	DG.add_path(['l1','t'])
#	assert DG.unlearned_dependency_tree('t',['11']) == set([])
	
	DG.add_path(['l1', 'u1', 't']) #learned, unlearned, target
	assert DG.unlearned_dependency_tree('t', ['l1']) == set(['u1'])
	
	assert DG.unlearned_dependency_tree('t',[]) == set(['l1','u1'])
#	assert DG.unlearned_dependency_tree('',['l1') == ???
	
	DG.add_path(['u1', 'u2', 'u1'])
	assert DG.unlearned_dependency_tree('t', ['l1']) == set(['u1', 'u2'])
	assert DG.unlearned_dependency_tree('t', []) == set(['u1', 'u2', 'l1'])
	assert DG.unlearned_dependency_tree('t', ['l1', 'u1']) == set(['u2'])
	DG.remove_edge('u2','u1')
	assert DG.unlearned_dependency_tree('u1', ['l1']) == set([])
	DG.add_path(['l1','u2','t'])
	assert DG.unlearned_dependency_tree('t', ['l1']) == set(['u1','u2'])
	
	#test with more than one learned node
	#test with more than one target?

