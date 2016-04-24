################################## IMPORTS ####################################
import json
from collections import OrderedDict

import networkx as nx
from lib.networkx.classes import digraph_extend

from lib import decorate

################################# HELPERS #####################################

#################################### MAIN #####################################


class _DAG (nx.DiGraph):


	def validate(self):
		if not nx.is_directed_acyclic_graph(self):
			raise TypeError('Not a Directed A(dir)cyclcic Graph!')
		return True

	def source(self): # finds any source in Directed A(dir)cyclic Graph
		self.validate() # it's important that there are no cycles!
		if not self.nodes():
			return None
		currentNode = self.nodes()[0]
		while not self.is_source(currentNode):
			currentNode = self.predecessor(currentNode)
		return currentNode

	def sources(self): # finds the sources in a Directed A(dir)cyclic Graph
		dag2 = self.copy()
		sources = set()
		while dag2.is_nonnull():
			source = dag2.source()
			sources.add(source)
			sourceAndDescendants = {source} | dag2.descendants(source)
			dag2 = dag2.subgraph( set(dag2.nodes()) - sourceAndDescendants )
		return sources

	def common_descendant_sources(self, nbunchA, nbunchB):
		return self.subgraph(self.common_descendants(nbunchA, nbunchB)).sources()

	def has_path(self, start, end):
		return nx.has_path(self, start, end)

	def remove_redundant_edges(self):
		for edge in self.edges():
			self.remove_edge(edge[0], edge[1])
			if not self.has_path(edge[0], edge[1]):
				self.add_edge(edge[0], edge[1])

	def depth_to_successors(self, axioms, learned_nodes):	#short sighted
		""" returns an ORDERED dict where the keys are depths (ordered greatest to least), values are lists of successors sharing that depth
		 nodes that are NOT descendants of the axioms will not appear in distance_dict.  This is OK.
		 
		:param acceptable_iter axioms: The "bottom" of our graph.  The distance from the axioms is the depth.
		:returns: bla bla bla
		:rtype: OrderedDict
		"""
		descendants_to_distance_dict = self.descendants_to_distance_dict(axioms)
		successors = self.successors(learned_nodes)
		successors_to_distance_dict = descendants_to_distance_dict_subdict_with_only_the_successors
		depth_to_successors_dict = helpers.reversed_dict(successors_to_distance_dict)
		return depth_to_successors_dict

	def choose_goal(self, axioms, learned_nodes):	#short sighted, depth-first
		#returns one immediate successor to learned_nodes which we should set as the new goal, chosen by depth, then learn count, then importance, then name
		self.validate_input_nodes(axioms) #do we need this?
		self.validate_input_nodes(learned_nodes)
		depth_to_successors_dict = self.short_sighted_depth_to_successors_dict(axioms, learned_nodes)
		deepest_successors = list(depth_to_successors_dict.items())[0][1]

		#now sort the deepest successors by learn count, then by importance, and finally name to break a tie
#if we need better efficiency consider creating DiGraph.learn_counts(targets, learned_nodes)
		def learn_count_sorter(successor):
			return (self.learn_count(successor, learned_nodes), -self.most_important_weight(successor), self.n(successor).id)
		goal = sorted(deepest_successors, key=learn_count_sorter)[0]
		return goal

	def learnable_pregoals(self, goal, learned_nodes):	#a pregoal is an unlearned dependency of the goal
		learnable_nodes = set(self.absolute_dominion(learned_nodes))
		prereqs = self.unlearned_dependency_tree(goal, learned_nodes)
		return set.intersection(learnable_nodes, prereqs)

	@decorate.record_elapsed_time
	def choose_learnable_pregoal(self, axioms, learned_nodes, goal=None):
		if not goal:
			goal = self.short_sighted_depth_first_choose_goal(axioms, learned_nodes)
		learnable_prereqs = self.learnable_prereqs(goal, learned_nodes)
		return self.most_important(1, learnable_prereqs)[0]

nx.DAG = _DAG
