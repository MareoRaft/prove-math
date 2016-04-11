################################## IMPORTS ####################################
import networkx as nx
import pytest

from lib.networkx.classes import dag
from lib.node import create_appropriate_node, Node

from collections import OrderedDict
#why is that needed?  we imported dag and dag already imported this

################################## HELPERS ####################################
def fill_sample_custom_nodes():
	#creates a graph with a handful of our custom node objects, but no edges
	pre_a = {"type":"theorem","description":"This is node aaaaaaaaaa","name":"A","importance":2}
	a = Node(pre_a)
	pre_b = {"type":"theorem","description":"This is node bbbbbbbbbb","name":"B","importance":4}
	b = create_appropriate_node(pre_b)
	pre_c = {"type":"theorem","description":"This is node cccccccccc","name":"C","importance":4}
	c = create_appropriate_node(pre_c)
	pre_d = {"type":"theorem","description":"This is node dddddddddd","name":"D","importance":6}
	d = create_appropriate_node(pre_d)
	pre_e = {"type":"theorem","description":"This is node eeeeeeeeee","name":"E","importance":8}
	e = Node(pre_e)
	DAG = nx.DAG()
	DAG.add_n(a)
	DAG.add_n(b)
	DAG.add_n(c)
	DAG.add_n(d)
	DAG.add_n(e)
	return DAG

#################################### MAIN #####################################
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

def test_sources():
	DAG = nx.DAG()
	assert DAG.sources() == set()

	DAG.add_path(['a', 'b', 'c', 'd'])
	assert DAG.sources() == {'a'}

	DAG.add_edge('z', 'd')
	assert DAG.sources() == {'a', 'z'}

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

def test_short_sighted_depth_to_successors_dict():
	DAG = nx.DAG()
	DAG.add_path(['axiom', 'one', 'two', 'three', 'four', 'five'])
	d = DAG.short_sighted_depth_to_successors_dict('axiom', ['two']) #notice axioms do not need to be in a list
	assert d == {3: ['three']} #does not need to be ordered in this case
	d = DAG.short_sighted_depth_to_successors_dict('axiom', ['two', 'four'])
	res = OrderedDict.fromkeys([5, 3])
	res[5] = ['five']
	res[3] = ['three']
	assert d == res
	d = DAG.short_sighted_depth_to_successors_dict('axiom', ['two', 'three'])
	assert d == {4: ['four']}
	
	DAG = nx.DAG()
	DAG.add_path(['axiom1', 'one', 'two', 'axiom2', 'three', 'four'])
	d = DAG.short_sighted_depth_to_successors_dict(['axiom1', 'axiom2'], ['three'])
	assert d == {2: ['four']} #depth is counted from the CLOSEST axiom
	
	DAG = nx.DAG()
	DAG.add_path(['axiom1', 'one', 'two', 'four', 'six'])
	DAG.add_path(['axiom2', 'three', 'four'])
	DAG.add_path(['axiom3', 'five', 'six'])
	d = DAG.short_sighted_depth_to_successors_dict(['axiom1', 'axiom2', 'axiom3'], ['one', 'two', 'four'])
	assert d == {2: ['six']} #returns 'six' even though 'six' is not learnable right now

def test_short_sighted_depth_first_choose_goal():
	DAG = fill_sample_custom_nodes()	
	#first sort by depth:
	DAG.add_path(['axiom', 'one', 'b'])
	DAG.add_path(['axiom', 'two', 'three', 'c'])
	assert DAG.short_sighted_depth_first_choose_goal(['axiom'], ['one', 'two', 'three']) == 'c'
	#make sure this case is symmetric and node id does not affect it:
	DAG.remove_nodes_from(['axiom', 'one', 'two', 'three'])
	DAG.add_path(['axiom', 'one', 'c'])
	DAG.add_path(['axiom', 'two', 'three', 'b'])
	assert DAG.short_sighted_depth_first_choose_goal(['axiom'], ['one', 'two', 'three']) == 'b'

	#next sort by learn count:
	DAG.remove_nodes_from(['axiom', 'one', 'two', 'three'])
	DAG.add_edges_from([
		('a', 'c'), ('a', 'd'), ('e', 'd')
	]) # d now has a higher learn count than c but the same depth (d is more important)
	assert DAG.short_sighted_depth_first_choose_goal(['a'], ['a']) == 'c'
	#again make sure this is symmetric:
	DAG.remove_edges_from([('a', 'c'), ('a', 'd'), ('e', 'd')])
	DAG.add_edges_from([
		('a', 'c'), ('a', 'd'), ('e', 'c')
	]) # c now has a higher learn count than d but the same depth (d still more important)
	assert DAG.short_sighted_depth_first_choose_goal(['a'], ['a']) == 'd'
	
	#then sort by importance:
	DAG.remove_edges_from([('a', 'c'), ('a', 'd'), ('e', 'c')])
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd')
	]) # same depth and learn count but d is more important than c
	assert DAG.short_sighted_depth_first_choose_goal(['a'], ['b']) == 'd'

	#finally sort by name
	DAG.remove_edges_from([('a', 'b'), ('b', 'c'), ('b', 'd')])
	DAG.add_edges_from([
		('a', 'd'), ('d', 'b'), ('d', 'c')
	])
	assert DAG.short_sighted_depth_first_choose_goal(['a'], ['d']) == 'b' #this goes in alphabetical order, unlike digraph.most_important which goes in reverse alphabetical

def test_learnable_prereqs():
	DAG = nx.DAG()
	DAG.add_path(['l1', 't'])
	with pytest.raises(ValueError):
		DAG.learnable_prereqs('t', [])
	with pytest.raises(nx.NetworkXError):
		DAG.learnable_prereqs(['t'], ['l1'])
	with pytest.raises(ValueError):
		DAG.learnable_prereqs('t', 'l1')
	assert DAG.learnable_prereqs('t', ['l1']) == {'t'}
	
	DAG = nx.DAG()
	DAG.add_edges_from([
		('l1', 't'), ('u1', 't') # learned, unlearned, target
	])
	assert DAG.learnable_prereqs('t', ['l1']) == set()
	
	DAG = nx.DAG()
	DAG.add_edges_from([
		('l1', 't'), ('l2', 'u1'), ('u1', 't'), ('u2', 't')
	])
	assert DAG.learnable_prereqs('t', ['l1', 'l2']) == {'u1'}

def test_choose_next_prereq():
	DAG = fill_sample_custom_nodes()
	DAG.add_edge('a', 'b')
	with pytest.raises(ValueError):
		print(DAG.choose_next_prereq(['b'], 'a'))
	assert DAG.choose_next_prereq(['b'], ['a']) == 'b'
	
	#first sort by learn count
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('a', 'd')
	])
	assert DAG.choose_next_prereq(['c', 'd'], ['a']) == 'd'
	
	#then sort by importance
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c'), ('a', 'd')
	])
	assert DAG.choose_next_prereq(['b', 'c', 'd'], ['a']) == 'd'
	
	#finally sort by name
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c')
	])
	assert DAG.choose_next_prereq(['b', 'c'], ['a']) == 'b'

def test_user_learn_suggestion():
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c')
	])
	with pytest.raises(ValueError):
		DAG.user_learn_suggestion(['a'], [])
	assert DAG.user_learn_suggestion(['a'], ['a']) == 'b'
		
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd')
	])
	assert DAG.user_learn_suggestion(['a'], ['b']) == 'd'
	
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd'), ('e', 'd')
	])
	assert DAG.user_learn_suggestion(['a'], ['b']) == 'c'
	
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd'), ('e', 'c'), ('e', 'd'), ('b', 'e')
	])
	assert DAG.user_learn_suggestion(['a'], ['b']) == 'e'
	
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c'), ('d', 'b'), ('e', 'c'), ('a', 'd'), ('a', 'e')
	])
	assert DAG.user_learn_suggestion(['a'], ['a']) == 'e'

# def test_short_sighted_depth_first_unlearned_sources():
# 	G = nx.DAG()
# 	G.add_path(['1left', '2left', '3left', 'left'])
# 	G.add_path(['a', 'b', 'left'])
# 	G.add_path(['a', 'b', 'right'])
# 	G.add_path(['1right', '2right', 'right']) # this is less effort to learm, so 1right should be returned
# 	assert G.short_sighted_depth_first_unlearned_sources(['a', 'b']) == ['1right']

# 	# now do the same test, but reverse the order of adding stuff onto graph
# 	G = nx.DAG()
# 	G.add_path(['1right', '2right', 'right']) # this is less effort to learm, so 1right should be returned
# 	G.add_path(['a', 'b', 'right'])
# 	G.add_path(['a', 'b', 'left'])
# 	G.add_path(['1left', '2left', '3left', 'left'])
# 	assert G.short_sighted_depth_first_unlearned_sources(['a', 'b']) == ['1right']

# 	# edge cases, empty graph?  null graph?


# def test_short_sighted_deepest_successors():
	# G = nx.DAG()
	# G.add_path(['a', 'b', 'c'])
	# axioms = ['a']
	# nodes = ['a', 'b']
	# assert G.short_sighted_deepest_successors(axioms, nodes) == {2: ['c']}
# 
	# G = nx.DAG()
	# G.add_path(['a', 'b', 'c'])
	# G.add_path(['s', 't', 'c'])
	# axioms = ['a', 't']
	# nodes = ['a', 't']
	# assert G.short_sighted_deepest_successors(axioms, nodes) == {1: ['b', 'c']}
# 
	# G = nx.DAG()
	# G.add_path(['a', 'b', 'c'])
	# G.add_path(['s', 't', 'c'])
	# G.add_path(['p', 't', 'a'])
	# axioms = ['a', 's']
	# nodes = ['p', 'a', 'b']
	# assert G.short_sighted_deepest_successors(axioms, nodes) == {
		# 1: ['t'],
		# 2: ['c']
	# }

