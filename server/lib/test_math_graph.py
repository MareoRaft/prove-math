############################ IMPORTS ############################
from collections import OrderedDict
import pytest
import networkx as nx

from lib.math_graph import MathGraph
from lib.node import create_appropriate_node, Node
from lib.user import User

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
	DAG = MathGraph()
	DAG.add_n(a)
	DAG.add_n(b)
	DAG.add_n(c)
	DAG.add_n(d)
	DAG.add_n(e)
	return DAG

############################## MAIN ##############################
def test_n():
	pass
	# TODO

def test_add_n():
	pass
	# TODO

def test_as_js_ready_dict():
	pre_a = {"type":"theorem","description":"This is node aaaaaaaaaa","name":"A","importance":3}
	a = create_appropriate_node(pre_a)
	pre_b = {"type":"theorem","description":"This is node bbbbbbbbbb","name":"B","importance":4}
	b = create_appropriate_node(pre_b)
	pre_c = {"type":"theorem","description":"This is node cccccccccc","name":"C","importance":4}
	c = create_appropriate_node(pre_c)

	DG = MathGraph()
	d = DG.as_js_ready_dict()
	assert d == {'nodes': [], 'links': []}

	DG = MathGraph()
	DG.add_n(a)
	d = DG.as_js_ready_dict()
	assert d == {'nodes': [a.__dict__], 'links': []}

	DG = MathGraph()
	DG.add_n(a)
	DG.add_n(b)
	d = DG.as_js_ready_dict()
	dl = d['links']
	dn = d['nodes']
	assert dl == []
	assert (dn == [a.__dict__, b.__dict__] or dn == [b.__dict__, a.__dict__])

	DG = MathGraph()
	DG.add_n(a)
	DG.add_n(b)
	DG.add_edge('a', 'b')
	d = DG.as_js_ready_dict()
	dl = d['links']
	dn = d['nodes']
	assert (dl == [{'source': 'a', 'target': 'b'}])
	assert (dn == [a.__dict__, b.__dict__] or dn == [b.__dict__, a.__dict__])

	DG = MathGraph()
	DG.add_n(a)
	DG.add_n(b)
	DG.add_n(c)
	DG.add_path(['a', 'b', 'c'])
	d = DG.as_js_ready_dict()
	dl = d['links']
	dn = d['nodes']
	assert (	#ordering is ambiguous so check each possibility
		dl == [{'source': 'a', 'target': 'b'}, {'source': 'b', 'target': 'c'}]
		or
		dl == [{'source': 'b', 'target': 'c'}, {'source': 'a', 'target': 'b'}]
		)
	assert (
		dn == [a.__dict__, b.__dict__, c.__dict__] or dn == [a.__dict__, c.__dict__, b.__dict__]
		or dn == [b.__dict__, a.__dict__, c.__dict__] or dn == [b.__dict__, c.__dict__, a.__dict__]
		or dn == [c.__dict__, a.__dict__, b.__dict__] or dn == [c.__dict__, b.__dict__, a.__dict__]
		)

def test_unlearned_dependency_tree():
	DG = MathGraph()
	DG.add_path(['l1', 't'])
	assert DG.unlearned_dependency_tree('t', ['l1']) == {'t'}

	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't']) #learned, unlearned, target
	with pytest.raises(nx.NetworkXError):
		DG.unlearned_dependency_tree('NotANode', ['l1'])
	with pytest.raises(nx.NetworkXError):
		DG.unlearned_dependency_tree(['t'], ['l1'])
	assert DG.unlearned_dependency_tree('t', ['l1']) == {'u1', 't'}
	with pytest.raises(ValueError):
		DG.unlearned_dependency_tree('t', 'l1')
	assert DG.unlearned_dependency_tree('t', []) == {'l1', 'u1', 't'}
	assert DG.unlearned_dependency_tree('t', ['NotANode', 'StillNotANode']) == {'l1', 'u1', 't'}

	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't'])
	DG.add_path(['u2', 'u1'])
	assert DG.unlearned_dependency_tree('t', ['l1']) == {'u1', 'u2', 't'}
	assert DG.unlearned_dependency_tree('t', []) == {'u1', 'u2', 'l1', 't'}
	assert DG.unlearned_dependency_tree('t', ['l1', 'u1']) == {'t'}

	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't'])
	DG.add_edge('u2', 't')
	assert DG.unlearned_dependency_tree('t', ['l1']) == {'u1', 'u2', 't'}

	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't'])
	DG.add_edge('u3', 'l1')
	assert DG.unlearned_dependency_tree('t', ['l1']) == {'u1', 't'}

	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't'])
	DG.add_path(['u4', 'l2', 't'])
	assert DG.unlearned_dependency_tree('t', ['l1', 'l2']) == {'u1', 't'}

def test_learn_count():
	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't'])
	with pytest.raises(nx.NetworkXError):
		DG.learn_count('NotANode', ['l1'])
	with pytest.raises(nx.NetworkXError):
		DG.learn_count(['t'], ['l1'])
	with pytest.raises(ValueError):
		DG.learn_count('t', 'l1')
	assert DG.learn_count('t', ['NotANode']) == 3
	assert DG.learn_count('t', []) == 3
	assert DG.learn_count('t', ['l1']) == 2
	assert DG.learn_count('t', ['u1']) == 1

def test_learn_counts():
	DG = MathGraph()
	DG.add_path(['l1', 'u1', 't'])
	assert DG.learn_counts(['t', 'u1'], []) == [3, 2]

def test_most_important():
	a = create_appropriate_node({"type":"theorem","description":"This is node aaaaaaaaaa","name":"A","importance":3})
	b = create_appropriate_node({"type":"theorem","description":"This is node bbbbbbbbbb","name":"B","importance":4})
	c = create_appropriate_node({"type":"theorem","description":"This is node cccccccccc","name":"C","importance":4})
	d = create_appropriate_node({"type":"theorem","description":"This is node dddddddddd","name":"D","importance":6})
	e = create_appropriate_node({"type":"theorem","description":"This is node eeeeeeeeee","name":"E","importance":8})
	f = create_appropriate_node({"type":"theorem","description":"This is node ffffffffff","name":"F","importance":8})

	# we will REUSE the SAME graph for below tests:
	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])

	#testing sort by node's own importance and id
	with pytest.raises(ValueError):
		DAG.most_important([], 1)

	# trivial test
	assert DAG.most_important(['a'], 1) == ['a']

	# test that number defaults to 1
	assert DAG.most_important(['a']) == ['a']

	# bad number
	with pytest.raises(ValueError):
		DAG.most_important(['a'], -1)

	# and more...
	assert DAG.most_important(['a', 'b']) == ['b']
	assert DAG.most_important(['a', 'b'], 2) == ['b', 'a']
	with pytest.raises(ValueError):
		DAG.most_important(['a', 'b'], 4) == ['b', 'a']
	assert DAG.most_important(['a', 'b', 'c'], 2) == ['c', 'b'] #sorts alphabetically, but remember we use reverse=True to sort by numerical importance so the alphabetical sort is reversed too
	assert DAG.most_important(['a', 'b', 'c', 'd']) == ['d']
	assert DAG.most_important(['a', 'b', 'c', 'd'], 2) == ['d', 'c']
	assert DAG.most_important(['a', 'b', 'c', 'd'], 3) == ['d', 'c', 'b']


	# using DIFFERENT graphs for the BELOW TESTS:

	#testing sort by weighted importance of neighbors when node's own importance is a tie
	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])
	DAG.add_edges_from([
			['a', 'c'], ['d', 'b']	#d is a more important neighbor than a, so b should be more important than c
	])
	node_list = ['b', 'c']
	assert DAG.most_important(node_list, 2) == ['b', 'c']

	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])
	DAG.add_edges_from([
			['c', 'a'], ['b', 'd']
	])
	node_list = ['b', 'c']
	assert DAG.most_important(node_list, 2) == ['b', 'c']

	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])
	DAG.add_edges_from([
			['c', 'a'], ['d', 'b']	#d is a more important neighbor than a but this time a is a descendant while d is only an ancestor; this time c should be more important than b
	])
	node_list = ['b', 'c']
	assert DAG.most_important(node_list, 2) == ['c', 'b']

	#remember that when the nodes being compared are neighbors with each other, we will get some shared common neighbors, although they have different distances to the two compared nodes
	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])
	DAG.add_edge('b', 'c')
	node_list = ['b', 'c']
	assert DAG.most_important(node_list, 2) == ['b', 'c']	#descendants are given more weight
	DAG.add_edge('c', 'b')
	assert DAG.most_important(node_list, 2) == ['c', 'b']	#now sorts (reverse) alphabetically because neighbor weights are symmetric

def test_choose_goal():
	# NOTE: our criteria for which goal to choose may change in the future.  In which case, some of the tests below may fail
	a = create_appropriate_node({"type":"theorem","description":"This is node aaaaaaaaaa","name":"A","importance":5})
	b = create_appropriate_node({"type":"theorem","description":"This is node bbbbbbbbbb","name":"B","importance":5})
	c = create_appropriate_node({"type":"theorem","description":"This is node cccccccccc","name":"C","importance":5})
	d = create_appropriate_node({"type":"theorem","description":"This is node dddddddddd","name":"D","importance":5})
	e = create_appropriate_node({"type":"theorem","description":"This is node eeeeeeeeee","name":"E","importance":5})
	f = create_appropriate_node({"type":"theorem","description":"This is node ffffffffff","name":"F","importance":5})

	# choose deepest goal
	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])
	DAG.add_path(['a', 'b', 'c'])
	DAG.add_path(['a', 'd', 'e', 'f'])
	assert DAG.choose_goal(['a'], ['b', 'd', 'e']) == 'f'

	# make sure this case is symmetric and node id does not affect it:
	DAG = MathGraph()
	DAG.add_n([a, b, c, d, e, f])
	DAG.add_path(['a', 'b', 'f'])
	DAG.add_path(['a', 'd', 'e', 'c'])
	assert DAG.choose_goal(['a'], ['b', 'd', 'e']) == 'c'

	# next sort by learn count:
	DAG = MathGraph()
	DAG.add_n([a, c, d, e])
	DAG.add_edges_from([
		('a', 'c'), ('a', 'd'), ('e', 'd')
	])
	d.importance = 10
	c.importance = 3
	# d now has a higher learn count than c but the same depth (d is more important)
	assert DAG.choose_goal(['a'], ['a']) == 'c'

	# again make sure this is symmetric:
	DAG = MathGraph()
	DAG.add_n([a, c, d, e])
	DAG.add_edges_from([
		('a', 'd'), ('a', 'c'), ('e', 'c')
	])
	d.importance = 10
	c.importance = 3
	# d now has a higher learn count than c but the same depth (d is more important)
	assert DAG.choose_goal(['a'], ['a']) == 'd'

	# then sort by importance:
	DAG = MathGraph()
	DAG.add_n([a, b, c, d])
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd')
	])
	d.importance = 10
	c.importance = 3
	# same depth and learn count but d is more important than c
	assert DAG.choose_goal(['a'], ['b']) == 'd'

	#finally sort by id
	DAG = MathGraph()
	DAG.add_n([a, b, c, d])
	DAG.add_edges_from([
		('a', 'd'),
		     ('d', 'b'),
		     ('d', 'c'),
	])
	# this goes in alphabetical order, unlike digraph.most_important which goes in reverse alphabetical
	assert DAG.choose_goal(['a'], ['d']) == 'b'

def test_learnable_pregoals():
	DAG = MathGraph()
	DAG.add_path(['l1', 't'])
	with pytest.raises(nx.NetworkXError):
		DAG.learnable_pregoals(['t'], ['l1'])
	with pytest.raises(ValueError):
		DAG.learnable_pregoals('t', 'l1')
	assert DAG.learnable_pregoals('t', []) == {'l1'}
	assert DAG.learnable_pregoals('t', ['l1']) == {'t'}

	DAG = MathGraph()
	DAG.add_edges_from([
		('l1', 't'), ('u1', 't') # learned, unlearned, target
	])
	assert DAG.learnable_pregoals('t', ['l1']) == {'u1'}

	DAG = MathGraph()
	DAG.add_edges_from([
		('l1', 't'), ('l2', 'u1'), ('u1', 't'), ('u2', 't')
	])
	assert DAG.learnable_pregoals('t', ['l1', 'l2']) == {'u1', 'u2'}

def test_choose_learnable_pregoals():
	DAG = fill_sample_custom_nodes()
	DAG.add_edge('a', 'b')
	with pytest.raises(ValueError):
		print(DAG.choose_learnable_pregoals(['b'], 'a'))
	assert DAG.choose_learnable_pregoals(['b'], ['a']) == ['b']

	#first sort by learn count
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('a', 'd')
	])
	assert DAG.choose_learnable_pregoals(['c', 'd'], ['a']) == ['d']

	#then sort by importance
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c'), ('a', 'd')
	])
	assert DAG.choose_learnable_pregoals(['b', 'c', 'd'], ['a']) == ['d']

	#finally sort by name
	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c')
	])
	assert DAG.choose_learnable_pregoals(['b', 'c'], ['a']) == ['b']

	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c')
	])
	with pytest.raises(ValueError):
		DAG.choose_learnable_pregoals(['a'], [])
	assert DAG.choose_learnable_pregoals(['a'], ['a']) == ['b']

	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd')
	])
	assert DAG.choose_learnable_pregoals(['a'], ['b']) == ['d']

	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd'), ('e', 'd')
	])
	assert DAG.choose_learnable_pregoals(['a'], ['b']) == ['c']

	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('b', 'c'), ('b', 'd'), ('e', 'c'), ('e', 'd'), ('b', 'e')
	])
	assert DAG.choose_learnable_pregoals(['a'], ['b']) == ['e']

	DAG = fill_sample_custom_nodes()
	DAG.add_edges_from([
		('a', 'b'), ('a', 'c'), ('d', 'b'), ('e', 'c'), ('a', 'd'), ('a', 'e')
	])
	assert DAG.choose_learnable_pregoals(['a'], ['a']) == ['e']

def test_nodes_to_send():
	# Need to complete!  Each option works independently but I did not try combining them!

	pmdag = fill_sample_custom_nodes()
	pre_set = {"type":"axiom","description":"__This is the node for set__","name":"set","importance":4}
	sset = create_appropriate_node(pre_set)
	pre_vertex = {"type":"axiom","description":"__This is the node for vertex__","name":"vertex","importance":4}
	vertex = create_appropriate_node(pre_vertex)
	pre_multiset = {"type":"axiom","description":"__This is the node for multiset__","name":"multiset","importance":4}
	multiset = create_appropriate_node(pre_multiset)
	pmdag.add_n(sset)
	pmdag.add_n(vertex)
	pmdag.add_n(multiset)

	pmdag.add_path(['a', 'b', 'c', 'e'])
	pmdag.add_path(['b', 'd', 'e'])
	pmdag.add_edges_from([
		('set', 'a'), ('vertex', 'a'), ('multiset', 'a')
	])

	greg = User({'type': 'facebook', 'id': 'test_pmdag_greg'})
	#helpers
	def reset_prefs(user): # sets preferences for minimal client nodes; should send learned nodes and starting nodes only
		user.set_prefs(
		{'subject': 'graph theory',
		'goal_id': None,
		'always_send_absolute_dominion': False,
		'always_send_learnable_pregoals': False,
		'send_learnable_pregoal_number': 1,
		'always_send_goal': False,
		'always_send_unlearned_dependency_tree_of_goal': False}
		)
	def reset_learned(user):
		for node_id in user.dict['learned_node_ids']:
			user.unlearn_node(node_id)

	# check starting nodes

	reset_learned(greg)
	reset_prefs(greg)
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == set()
	greg.set_pref({'subject': None})
	with pytest.raises(ValueError):
		pmdag.nodes_to_send(greg)

	greg.set_pref({'subject': 'not a real subject'})
	with pytest.raises(ValueError):
		pmdag.nodes_to_send(greg)

	# check learned nodes

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b'}

	# check absolute dominion

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.set_pref({'always_send_absolute_dominion': True})
	# should now send learnable successors of learned nodes
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b'}

	# check learnable pregoals

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	greg.set_pref({'always_send_learnable_pregoals': True})
	greg.set_pref({'goal_id': 'e'}) # using a manually set goal
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'd'} # d is chosen over c because it is more important

	greg.set_pref({'send_learnable_pregoal_number': 2}) # ask for more than one pregoal
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'c', 'd'} # c and d both chosen as pregoals

	greg.set_pref({'goal_id': None}) # choses a goal without setting it
	# in this case d should be chosen as the goal (because d and c are the only successors of learned_nodes and d is more important)
	greg.set_pref({'send_learnable_pregoal_number': 1})
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'd'} # d is chosen as the goal, then also set as the pregoal

	# check always send goal

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	greg.set_pref({'always_send_goal': True})
	greg.set_pref({'goal_id': 'e'})
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'e'}

	# check always send dependency tree of goal

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	greg.set_pref({'always_send_unlearned_dependency_tree_of_goal': True})
	greg.set_pref({'goal_id': 'e'})
	nodes = pmdag.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'c', 'd', 'e'}

