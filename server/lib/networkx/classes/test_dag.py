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

