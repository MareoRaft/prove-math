################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import dag

#################################### MAIN #####################################
def test_validate():
	DAG = nx.DAG()
	DAG.add_edges_from([
		['a', 'b'],
		['b', 'c'],
		['c', 'd'],
	])
	assert DAG.validate()

	DAG.add_edge('d', 'a')
	try:
		DAG.validate() # this crashes the program unless the specific error is listed below.
		assert False # this line always fails.  The point is that we don't want this line to ever run.  If it does, something went wrong!
	except TypeError as e:
		assert str(e) == 'Not a Directed A(dir)cyclcic Graph!'

def test_source():
	DAG = nx.DAG()
	assert DAG.source() == None

	DAG.add_edges_from([
		['a', 'b'],
		['b', 'c'],
		['c', 'd'],
	])
	assert DAG.source() == 'a'
	assert DAG.source() != 'd'

def test_sources():
	DAG = nx.DAG()
	assert DAG.sources() == set()

	DAG.add_edges_from([
		['a', 'b'],
		['b', 'c'],
		['c', 'd'],
	])
	assert DAG.sources() == {'a'}

	DAG.add_edge('z', 'd')
	assert DAG.sources() == {'a', 'z'}

def test_common_descendant_sources():
	DAG = nx.DAG()
	DAG.add_edges_from([
		['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'z'],
		['c', 't'], ['t', 'w'], ['w', 'x'], ['x', 'y'], ['y', 'z'],
	])
	assert DAG.common_descendant_sources('a', 'c') == {'d', 't'}
	assert DAG.common_descendant_sources('d', 't') == {'z'}

	DAG = nx.DAG()
	DAG.add_edges_from([
		['A', 'one'], ['one', 'mid'], ['mid', 'end'],
		['B', 'one'],
		['A', 'two'], ['two', 'mid'], ['mid', 'end'],
		['B', 'two'],
		['t', 'mid'],
	])
	assert DAG.common_descendant_sources('A', 'B') == {'one', 'two'}
	# assert DAG.common_descendant_sources({'A', 'one'}, 'B') == {'two'} # networkx won't accept nbunches :(

def test_remove_redundant_edges():
	DAG = nx.DAG()
	DAG.add_edges_from([
		['a', 'b'], ['b', 'c'],
		['a', 'c'], # redundant!
	])
	DAG.remove_redundant_edges()
	assert ('a', 'b') in DAG.edges()
	assert ('b', 'c') in DAG.edges()
	assert ('a', 'c') not in DAG.edges()

	# take 2
	DAG = nx.DAG()
	DAG.add_edges_from([
		['a', 'b'], ['b', 'c'], ['c', 'd'],
		['a', 'd'], # redundant!
	])
	DAG.remove_redundant_edges()
	assert {('a', 'b'), ('b', 'c'), ('c', 'd')} <= set(DAG.edges())
	assert ('a', 'd') not in DAG.edges()

	# take 3
	DAG = nx.DAG()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'd'),
		('a', 'c'), ('c', 'd'),
		('a', 'd'), # redundant!
	])
	DAG.remove_redundant_edges()
	assert {('a', 'b'), ('b', 'd'), ('a', 'c'), ('c', 'd')} <= set(DAG.edges())
	assert ('a', 'd') not in DAG.edges()

	# take 4
	DAG.add_edges_from((
		('a', 'b'), ('b', 'c'), ('c', 'd'), 			('d', 'z'),
								('c', 't'), ('t', 'y'), ('y', 'z'),

		('a', 'd'), # redundant!
		('c', 'y'),
		('b', 'z'),
	))
	DAG.remove_redundant_edges()
	assert {('a', 'b'), ('b', 'c'), ('c', 'd'), 			('d', 'z'),
									('c', 't'), ('t', 'y'), ('y', 'z'),} == set(DAG.edges())

def test_single_source_shortest_path_lengths():
	G=nx.DAG()
	G.add_path([0,1,2,3,4,5,6,7,8,9])
	x=G.single_source_shortest_path_length(5,3)
	assert len(x)==7
	assert x=={3: 2, 4: 1, 5: 0, 6: 1, 7: 2, 8: 3, 2: 3}


