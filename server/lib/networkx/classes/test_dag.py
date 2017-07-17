############################ IMPORTS ############################
import networkx as nx
import pytest

from lib.networkx.classes import dag
from lib.node import create_appropriate_node, Node

from collections import OrderedDict

############################ HELPERS ############################
def fill_sample_custom_nodes():
	# creates a graph with a handful of our custom Node objects, but no edges
	pre_a = {"type":"theorem","description":"This is node aaaaaaaaaa","name":"A","importance":3}
	a = create_appropriate_node(pre_a)
	pre_b = {"type":"theorem","description":"This is node bbbbbbbbbb","name":"B","importance":4}
	b = create_appropriate_node(pre_b)
	pre_c = {"type":"theorem","description":"This is node cccccccccc","name":"C","importance":4}
	c = create_appropriate_node(pre_c)
	pre_d = {"type":"theorem","description":"This is node dddddddddd","name":"D","importance":6}
	d = create_appropriate_node(pre_d)
	pre_e = {"type":"theorem","description":"This is node eeeeeeeeee","name":"E","importance":8}
	e = create_appropriate_node(pre_e)
	DAG = nx.DAG()
	DAG.add_n(a)
	DAG.add_n(b)
	DAG.add_n(c)
	DAG.add_n(d)
	DAG.add_n(e)
	return DAG

############################## MAIN ##############################
def test_validate():
	DAG = nx.DAG()
	DAG.add_path(['a', 'b', 'c', 'd'])
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

	DAG.add_path(['a', 'b', 'c', 'd'])
	assert DAG.source() == 'a'
	assert DAG.source() != 'd'

def test_common_descendant_sources():
	DAG = nx.DAG()
	DAG.add_path(['a', 'b', 'c', 'd', 'z'])
	DAG.add_path(          ['c', 't', 'w', 'x', 'y', 'z'])
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
		['a',             'c'], # redundant!
	])
	DAG.remove_redundant_edges()
	assert ('a', 'b') in DAG.edges()
	assert ('b', 'c') in DAG.edges()
	assert ('a', 'c') not in DAG.edges()

	# take 2
	DAG = nx.DAG()
	DAG.add_edges_from([
		['a', 'b'], ['b', 'c'], ['c', 'd'],
		['a',                         'd'], # redundant!
	])
	DAG.remove_redundant_edges()
	assert {('a', 'b'), ('b', 'c'), ('c', 'd')} <= set(DAG.edges())
	assert ('a', 'd') not in DAG.edges()

	# take 3
	DAG = nx.DAG()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'd'),
		('a', 'c'), ('c', 'd'),
		('a',             'd'), # redundant!
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

def test_depth_to_successors_dict():
	DAG = nx.DAG()
	DAG.add_path(['axiom', 'one', 'two', 'three', 'four', 'five'])
	d = DAG.depth_to_successors_dict('axiom', ['two']) # notice axioms do not need to be in a list
	assert type(d).__name__ == 'OrderedDict'
	assert d == {3: {'three'}} # does not need to be ordered in this case
	d = DAG.depth_to_successors_dict('axiom', ['two', 'four'])
	assert d == OrderedDict([
		(5, {'five'}),
		(3, {'three'}),
	])

	d = DAG.depth_to_successors_dict('axiom', ['two', 'three'])
	assert d == OrderedDict([
		(4, {'four'}),
	])

	DAG = nx.DAG()
	DAG.add_path(['axiom1', 'one', 'two', 'axiom2', 'three', 'four'])
	d = DAG.depth_to_successors_dict(['axiom1', 'axiom2'], ['three'])
	# depth is counted from the CLOSEST axiom
	assert d == OrderedDict([
		(2, {'four'}),
	])
	d = DAG.depth_to_successors_dict(['axiom1', 'axiom2'], ['one'])
	assert d == OrderedDict([
		(2, {'two'}),
	])
	d = DAG.depth_to_successors_dict(['axiom1', 'axiom2'], ['two'])
	assert d == OrderedDict([
		(0, {'axiom2'}),
	])

	DAG = nx.DAG()
	DAG.add_path(['axiom1', 'one', 'two', 'four', 'six'])
	DAG.add_path(['axiom2', 'three', 'four'])
	DAG.add_path(['axiom3', 'five', 'six'])
	d = DAG.depth_to_successors_dict(['axiom1', 'axiom2', 'axiom3'], ['one', 'two', 'four'])
	assert d == OrderedDict([
		(2, {'six'}),
	])

def test_is_forward_order():
	DAG = nx.DAG()
	assert DAG.is_forward_order([])

	DAG = nx.DAG()
	DAG.add_path(['one', 'two', 'three', 'four'])
	assert DAG.is_forward_order([])
	assert DAG.is_forward_order(['one'])
	assert DAG.is_forward_order(['one', 'two'])
	assert DAG.is_forward_order(['one', 'three'])
	assert DAG.is_forward_order(['two', 'four'])
	assert not DAG.is_forward_order(['two', 'one'])
	assert not DAG.is_forward_order(['two', 'two'])
	assert not DAG.is_forward_order(['one', 'two', 'four', 'three'])

	DAG = nx.DAG()
	DAG.add_path(['1', 'a2', 'a3', '4'])
	DAG.add_path(['1', 'b2', 'b3', '4'])
	DAG.add_node('float')
	assert DAG.is_forward_order(['b3', 'a2'])
	assert DAG.is_forward_order(['float', '4'])
	assert DAG.is_forward_order(['4', 'float'])
	assert DAG.is_forward_order(['1', 'float', 'a3', 'b2', 'b3', '4'])
	assert not DAG.is_forward_order(['4', 'a2'])

