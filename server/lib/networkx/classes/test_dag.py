################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import dag

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

#########################################################################################
#########################################################################################
def test_short_sighted_depth_to_successors_dict():
	#DAG = nx.DAG()
	#assert DAG.short_sighted_depth_to_successors_dict(axioms, learned_nodes)
	return

def test_short_sighted_depth_first_choose_goal():
	#DAG = nx.DAG()
	#assert DAG.short_sighted_depth_first_choose_goal(axioms, learned_nodes)
	return

def test_learnable_prereqs():
	#DAG = nx.DAG()
	#assert DAG.learnable_prereqs(goal, learned_nodes)
	return

def test_choose_next_prereq():
	#DAG = nx.DAG()
	#assert DAG.choose_next_prereq(prereqs, learned_nodes)
	return

def test_user_learn_suggestion():
	#DAG = nx.DAG()
	#assert DAG.user_learn_suggestion(axioms, learned_nodes, goal)
	return
#########################################################################################
#########################################################################################

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

