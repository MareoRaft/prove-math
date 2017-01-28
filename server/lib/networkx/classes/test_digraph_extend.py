########################### IMPORTS #############################
import networkx as nx
import pytest

from lib.networkx.classes import digraph_extend
from lib.node import create_appropriate_node, Node
from lib.networkx.classes.testing_helper import fill_sample_custom_nodes

############################# MAIN ##############################
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
	assert DG.predecessor('y') == None
	with pytest.raises(nx.NetworkXError):
		assert DG.predecessor('NotANode')

def test_successor():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
	])
	assert DG.successor('c') in {'d', 'L'}
	assert DG.successor('d') == None
	with pytest.raises(nx.NetworkXError):
		assert DG.successor('NotANode')

def test_predecessors():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
		['a', 'b']
	])
	#test bad inputs
	with pytest.raises(nx.NetworkXError):
		DG.predecessors('NotANode')
	with pytest.raises(nx.NetworkXError):
		DG.predecessors(['NotANode'])
	with pytest.raises(nx.NetworkXError):
		DG.predecessors(['c', 'NotANode'])
	#test single input
	assert DG.predecessors([]) == set()
	assert DG.predecessors('y') == set()
	assert DG.predecessors('d') == {'c'}
	assert DG.predecessors('c') == {'y', 't'}
	assert DG.predecessors(['c']) == {'y', 't'}
	#test multiple inputs
	assert DG.predecessors(['y', 'd']) == {'c'}
	assert DG.predecessors(['d', 'c']) == {'y', 't'}
	assert DG.predecessors(['c', 'b']) == {'y', 't', 'a'}

def test_successors():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
		['a', 'b']
	])
	#test bad inputs
	with pytest.raises(nx.NetworkXError):
		DG.successors('NotANode')
	with pytest.raises(nx.NetworkXError):
		DG.successors(['NotANode'])
	with pytest.raises(nx.NetworkXError):
		DG.successors(['c', 'NotANode'])
	#test single input
	assert DG.successors([]) == set()
	assert DG.successors('d') == set()
	assert DG.successors('y') == {'c'}
	assert DG.successors('c') == {'L', 'd'}
	assert DG.successors(['c']) == {'L', 'd'}
	#test multiple inputs
	assert DG.successors(['y', 'd']) == {'c'}
	assert DG.successors(['y', 'c']) == {'L', 'd'}
	assert DG.successors(['c', 'a']) == {'L', 'd', 'b'}

def test_sources():
	DG = nx.DiGraph()
	assert DG.sources() == set()

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'd'])
	assert DG.sources() == {'a'}

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'd'])
	DG.add_edge('z', 'd')
	assert DG.sources() == {'a', 'z'}

	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b'])
	assert DG.sources() == set()

	DG = nx.DiGraph()
	DG.add_edge('s', 'a')
	DG.add_cycle(['a', 'b', 'c', 'd'])
	DG.add_edge('d', 't')
	assert DG.sources() == {'s'}

def test_sinks():
	DG = nx.DiGraph()
	assert DG.sinks() == set()

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'd'])
	assert DG.sinks() == {'d'}

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c', 'd'])
	DG.add_edge('z', 'd')
	assert DG.sinks() == {'d'}

	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b'])
	assert DG.sinks() == set()

	DG = nx.DiGraph()
	DG.add_edge('s', 'a')
	DG.add_cycle(['a', 'b', 'c', 'd'])
	DG.add_edge('d', 't')
	assert DG.sinks() == {'t'}

def test_anydirectional_neighbors():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['y', 'c'], ['c', 'L'],
		['t', 'c'], ['c', 'd'],
		['a', 'b'], ['b', 'e']
	])
	DG.add_node('x')
	#test bad inputs
	with pytest.raises(nx.NetworkXError):
		DG.anydirectional_neighbors('NotANode')
	with pytest.raises(nx.NetworkXError):
		DG.anydirectional_neighbors(['NotANode'])
	with pytest.raises(nx.NetworkXError):
		DG.anydirectional_neighbors(['c', 'NotANode'])
	#test single input
	assert DG.anydirectional_neighbors([]) == set()
	assert DG.anydirectional_neighbors('x') == set()
	assert DG.anydirectional_neighbors('d') == {'c'}
	assert DG.anydirectional_neighbors('y') == {'c'}
	assert DG.anydirectional_neighbors('c') == {'y', 't', 'L', 'd'}
	assert DG.anydirectional_neighbors(['c']) == {'y', 't', 'L', 'd'}
	#test multiple inputs
	assert DG.anydirectional_neighbors(['y', 'x']) == {'c'}
	assert DG.anydirectional_neighbors(['y', 'd']) == {'c'}
	assert DG.anydirectional_neighbors(['y', 'c']) == {'t', 'L', 'd'}
	assert DG.anydirectional_neighbors(['c', 'a']) == {'y', 't', 'L', 'd', 'b'}

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

	p = DG.shortest_anydirectional_path(['y', 'c'], ['L', 'd'])
	assert p == ['c', 'L'] or p == ['c', 'd']
	assert DG.shortest_anydirectional_path({'c', 'y'}, 'd') == ['c', 'd']

	DG.add_node('z')
	assert DG.shortest_anydirectional_path('z', 'c') == None

def test_ancestors():
	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])

	#testing nonexistent inputs:
	with pytest.raises(nx.NetworkXError):
		DG.ancestors('NotANode')
	with pytest.raises(nx.NetworkXError):
		DG.ancestors(['NotANode'])
	with pytest.raises(nx.NetworkXError):
		DG.ancestors(['x', 'NotANode', 'z'])

	#existing inputs:
	assert DG.ancestors([]) == set()
	assert DG.ancestors('z') == {'x', 'y'}
	assert DG.ancestors('y') == {'x'}
	assert DG.ancestors('x') == set()
	assert DG.ancestors(['x']) == set()

	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])
	DG.add_edges_from([
		['a', 'x'], ['b', 'y'], ['c', 'z']
	])
	assert DG.ancestors('z') == {'y', 'x', 'c', 'b', 'a'}
	assert DG.ancestors('y') == {'x', 'b', 'a'}
	assert DG.ancestors(['y', 'x']) == {'b', 'a'}

	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])
	DG.add_path(['a', 'b', 'c'])	#disconnected paths
	assert DG.ancestors(['c', 'z']) == {'b', 'a', 'y', 'x'}
	assert DG.ancestors(['a', 'x']) == set()
	assert DG.ancestors(['a', 'y']) == {'x'}
	DG.add_path(['x', 'b'])
	assert DG.ancestors(['c', 'z']) == {'b', 'a', 'y', 'x'}

def test_common_ancestors():
	DG = nx.DiGraph()
	DG.add_path(['a', 'x'])
	DG.add_path(['b', 'y'])

	#testing nonexistent inputs:
	with pytest.raises(nx.NetworkXError):
		DG.common_ancestors(['NotANode'], 'y')
	with pytest.raises(nx.NetworkXError):
		DG.common_ancestors('NotANode','StillNotANode')
	#existing inputs:
	assert DG.common_ancestors([],'y') == set()
	assert DG.common_ancestors('x', 'y') == set()
	assert DG.common_ancestors(['x', 'y'], 'x') == {'a'}

	DG = nx.DiGraph()
	DG.add_nodes_from(['x', 'y'])
	assert DG.common_ancestors('x', 'y') == set()

	DG = nx.DiGraph()
	DG.add_edges_from([['a', 'x'], ['c', 'y']])
	assert DG.common_ancestors('x', 'y') == set()

	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'x'], ['b', 'x'], ['b', 'y'], ['c', 'y']
	])
	assert DG.common_ancestors('x', 'y') == {'b'}

	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'x'], ['b', 'x'],
		['b', 'y'], ['c', 'y'],
		['d', 'b']
	])
	assert DG.common_ancestors('x', 'y') == {'b','d'}

	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'x'], ['b', 'y'],
		['b', 'z'], ['c', 'z']
	])
	assert DG.common_ancestors(['x', 'y'], 'z') == {'b'}
	DG.add_edge('a', 'z')
	assert DG.common_ancestors(['x', 'y'], 'z') == {'a', 'b'}

def test_descendants():
	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])

	#testing nonexistent inputs:
	with pytest.raises(nx.NetworkXError):
		DG.descendants('NotANode')
	with pytest.raises(nx.NetworkXError):
		DG.descendants(['NotANode'])
	with pytest.raises(nx.NetworkXError):
		DG.descendants(['x', 'NotANode', 'z']);

	#existing inputs:
	assert DG.descendants([]) == set()
	assert DG.descendants('x') == {'y', 'z'}
	assert DG.descendants('y') == {'z'}
	assert DG.descendants('z') == set()

	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])
	DG.add_edges_from([
			['x', 'a'], ['y', 'b'], ['z', 'c']
	])
	assert DG.descendants('x') == {'y', 'z', 'a', 'b', 'c'}
	assert DG.descendants('y') == {'z', 'b', 'c'}

	DG = nx.DiGraph()
	DG.add_path(['x', 'y', 'z'])
	DG.add_path(['a', 'b', 'c'])
	assert DG.descendants(['a', 'z']) == {'b', 'c'}
	assert DG.descendants(['c', 'z']) == set()
	DG.add_path(['x', 'b'])
	assert DG.descendants(['a', 'z']) == {'b', 'c'}

def test_common_descendants():
	DG = nx.DiGraph()
	DG.add_path(['x', 'a'])
	DG.add_path(['y', 'b'])

	#testing nonexistent inputs:
	with pytest.raises(nx.NetworkXError):
		DG.common_descendants(['NotANode'], 'y')
	with pytest.raises(nx.NetworkXError):
		DG.common_descendants('NotANode','StillNotANode')
	#existing inputs:
	assert DG.common_descendants([],'y') == set()
	assert DG.common_descendants('x', 'y') == set()
	assert DG.common_descendants(['x', 'y'], 'x') == {'a'}

	DG = nx.DiGraph()
	DG.add_nodes_from(['x', 'y'])
	assert DG.common_descendants('x', 'y') == set()

	DG = nx.DiGraph()
	DG.add_edges_from([['x', 'a'], ['y', 'c']])
	assert DG.common_descendants('x', 'y') == set()

	DG = nx.DiGraph()
	DG.add_edges_from([
		['x', 'a'], ['x', 'b'], ['y', 'b'], ['y', 'c']
	])
	assert DG.common_descendants('x', 'y') == {'b'}

	DG = nx.DiGraph()
	DG.add_edges_from([
		['x', 'a'], ['x', 'b'],
		['y', 'b'], ['y', 'c'],
		['b', 'd']
	])
	assert DG.common_descendants('x', 'y') == {'b','d'}

	DG = nx.DiGraph()
	DG.add_edges_from([
		['x', 'a'], ['y', 'b'],
		['z', 'b'], ['z', 'c']
	])
	assert DG.common_descendants(['x', 'y'], 'z') == {'b'}
	DG.add_edge('z', 'a')
	assert DG.common_descendants(['x', 'y'], 'z') == {'a', 'b'}

def test_relatives_to_distance_dict():
	G = nx.DiGraph()
	G = nx.path_graph(10, create_using=G)
	x = G.relatives_to_distance_dict(5, 3)
	assert len(x) == 7
	assert x == {
		2: 3,
		3: 2,
		4: 1,
		5: 0,
		6: 1,
		7: 2,
		8: 3,
	}

	x = G.relatives_to_distance_dict([3, 4], 2)
	assert len(x) == 6
	assert x == {
		1: 2,
		2: 1,
		3: 0,
		4: 0,
		5: 1,
		6: 2,
	}

def test_descendants_to_distance_dict():
	G = nx.DiGraph()
	G = nx.path_graph(7, create_using=G)
	d = G.descendants_to_distance_dict([3], 2)
	assert d == {3:0, 4:1, 5:2}
	d = G.descendants_to_distance_dict([3, 4], 2)
	assert d == {3:0, 4:0, 5:1, 6:2}

	G = nx.DiGraph()
	G.add_path(['a', 'y', 'd'])
	G.add_path(['a', 'l', 'x'])
	G.add_path(['a', 'c'])
	G.add_path(['b', 'c'])
	G.add_path(['b', 'd', 'l'])
	G.add_path(['b', 't', 'x'])
	d = G.descendants_to_distance_dict(['a', 'b'])
	assert d == {
		'a': 0, 'b': 0,
		'c': 1, 'y': 1, 'd': 1, 'l': 1, 't': 1,
		'x': 2,
	}

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
