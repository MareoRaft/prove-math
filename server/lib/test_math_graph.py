############################ IMPORTS ############################
import pytest
import networkx as nx

from lib.math_graph import MathGraph
from lib.node import create_appropriate_node
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
	G = MathGraph()
	G.add_n(a)
	G.add_n(b)
	G.add_n(c)
	G.add_n(d)
	G.add_n(e)
	return G

############################## MAIN ##############################
def test_nodes_to_send():
	# Need to complete!  Each option works independently but I did not try combining them!

	MG = fill_sample_custom_nodes()
	pre_set = {"type":"axiom","description":"__This is the node for set__","name":"set","importance":4}
	sset = create_appropriate_node(pre_set)
	pre_vertex = {"type":"axiom","description":"__This is the node for vertex__","name":"vertex","importance":4}
	vertex = create_appropriate_node(pre_vertex)
	pre_multiset = {"type":"axiom","description":"__This is the node for multiset__","name":"multiset","importance":4}
	multiset = create_appropriate_node(pre_multiset)
	MG.add_n(sset)
	MG.add_n(vertex)
	MG.add_n(multiset)

	MG.add_path(['a', 'b', 'c', 'e'])
	MG.add_path(['b', 'd', 'e'])
	MG.add_edges_from([
		('set', 'a'), ('vertex', 'a'), ('multiset', 'a')
	])

	greg = User({'type': 'local', 'id': None})

	#helpers
	def reset_prefs(user): # sets preferences for minimal client nodes; should send learned nodes and starting nodes only
		user.set_prefs({
			'subject': 'graph theory',
			'goal_id': None,
			'always_send_learnable_successors': False,
			'always_send_learnable_pregoals': False,
			'send_learnable_pregoal_number': 1,
			'always_send_goal': False,
			'always_send_unlearned_dependency_tree_of_goal': False,
		})
	def reset_learned(user):
		for node_id in user.dict['learned_node_ids']:
			user.unlearn_node(node_id)

	# check starting nodes

	reset_learned(greg)
	reset_prefs(greg)
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == set()
	greg.set_pref({'subject': None})
	with pytest.raises(ValueError):
		MG.nodes_to_send(greg)

	greg.set_pref({'subject': 'not a real subject'})
	with pytest.raises(ValueError):
		MG.nodes_to_send(greg)

	# check learned nodes

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b'}

	# check absolute dominion

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.set_pref({'always_send_learnable_successors': True})
	# should now send learnable successors of learned nodes
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b'}

	# check learnable pregoals

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	greg.set_pref({'always_send_learnable_pregoals': True})
	greg.set_pref({'goal_id': 'e'}) # using a manually set goal
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'd'} # d is chosen over c because it is more important

	greg.set_pref({'send_learnable_pregoal_number': 2}) # ask for more than one pregoal
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'c', 'd'} # c and d both chosen as pregoals

	greg.set_pref({'goal_id': None}) # choses a goal without setting it
	# in this case d should be chosen as the goal (because d and c are the only successors of learned_nodes and d is more important)
	greg.set_pref({'send_learnable_pregoal_number': 1})
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'd'} # d is chosen as the goal, then also set as the pregoal

	# check always send goal

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	greg.set_pref({'always_send_goal': True})
	greg.set_pref({'goal_id': 'e'})
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'e'}

	# check always send dependency tree of goal

	reset_learned(greg)
	reset_prefs(greg)
	greg.learn_node('a')
	greg.learn_node('b')
	greg.set_pref({'always_send_unlearned_dependency_tree_of_goal': True})
	greg.set_pref({'goal_id': 'e'})
	nodes = MG.nodes_to_send(greg).difference({'set', 'multiset', 'vertex'})
	assert nodes == {'a', 'b', 'c', 'd', 'e'}

