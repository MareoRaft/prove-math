################################## IMPORTS ####################################
import json
from collections import OrderedDict

import networkx as nx
from lib.networkx.classes import digraph_extend

from lib import decorate
from lib import helper

################################# HELPERS #####################################

#################################### MAIN #####################################


class _DAG (nx.DiGraph):


	@decorate.record_elapsed_time
	def importance_weight(self, node):
		distance_from_node = 0
		current_depth_nodes = {node}
		already_counted_nodes = set() # needed in case there are any cycles
		predecessors = {node}
		successors = {node}	#kept separate because descendants are given more weight than ancestors in asessing a node's importance
		ANCESTORS_DESCENDANTS_WEIGHT_FRACTION = 1/6
		NEIGHBOR_NORMALIZATION_FRACTION = 1/10 #rescales the sum of all neighbor importances to match the scale of the original node's own importance, i.e. [1,10]
		EXPECTED_NEIGHBORS_PER_NODE = 3

		norm_importances = [self.n(node).importance] #normalized importance of the nodes in each depth level
		SEARCH_DEPTH_LIMIT = 4
		while distance_from_node < SEARCH_DEPTH_LIMIT:
			distance_from_node += 1
			if predecessors:
				predecessors = self.predecessors(predecessors) - already_counted_nodes	#needed in case there are any cycles
			else:
				predecessors = set()
			if successors:
				successors = self.successors(successors) - already_counted_nodes
			else:
				successors = set()
			if (len(successors) + len(predecessors)) == 0:	#no more neighbors, don't look any further
				norm_importances.append(0)
				break
			predecessors_importances = [ANCESTORS_DESCENDANTS_WEIGHT_FRACTION * self.n(n).importance for n in predecessors]
			successors_importances = [(1-ANCESTORS_DESCENDANTS_WEIGHT_FRACTION) * self.n(n).importance for n in successors]	#weighted toward descendants
			current_depth_importances = predecessors_importances + successors_importances

			current_depth_normalized_sum = sum(current_depth_importances) * NEIGHBOR_NORMALIZATION_FRACTION / (EXPECTED_NEIGHBORS_PER_NODE**distance_from_node)
			#As distance increases there are exponentially more neighbors.  The 1/(EXPECTED_NEIGHBORS_PER_NODE**distance) term counteracts this.
			norm_importances.append(current_depth_normalized_sum)

			already_counted_nodes = already_counted_nodes.union(predecessors)
			already_counted_nodes = already_counted_nodes.union(successors)
		weighted_importances = [(importance/(index+1)**2) for index, importance in enumerate(norm_importances)]	#normalized importance of the nodes in each depth level, weighted against distance from node
		neighbors_weight = sum(weighted_importances)
		return neighbors_weight #(neighbors_weight, self.n(node).id)

	@decorate.record_elapsed_time
	def most_important(self, nbunch, number=1):
		def most_important_sorter(node):
			return (self.importance_weight(node), self.n(node).id)
		if number <= 0:
			raise ValueError('Must give number > 0')
		if len(nbunch) < number:
			raise ValueError('Asked for more nodes than you provided')
		nodes_by_importance = sorted(nbunch, key=most_important_sorter, reverse=True)
		return nodes_by_importance[:number]

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

	@decorate.record_elapsed_time
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

	@decorate.record_elapsed_time
	def remove_redundant_edges(self): # We need to be careful not to perform this on a live graph, since it temporarily alters the graph.
		for edge in self.edges():
			self.remove_edge(edge[0], edge[1])
			if not self.has_path(edge[0], edge[1]):
				self.add_edge(edge[0], edge[1])

	@decorate.record_elapsed_time
	def depth_to_successors_dict(self, axioms, learned_nodes):	# short sighted
		"""
		:param acceptable_iter axioms: The "bottom" of our graph.  The distance from the axioms is the depth.
		:returns: A dictionary where the keys are depths (ordered greatest to least), values are lists of successors sharing that depth.
		:rtype: OrderedDict

		*Note: nodes that are NOT descendants of the axioms will not appear in the dictionary.  This is OK.
		"""
		descendants_to_distance_dict = self.descendants_to_distance_dict(axioms)
		successors = self.successors(learned_nodes)
		successors_to_distance_dict = {k:v for k,v in descendants_to_distance_dict.items() if k in successors}
		depth_to_successors_dict = helper.reversed_dict(successors_to_distance_dict)
		return OrderedDict(sorted(depth_to_successors_dict.items(), key=lambda t: t[0], reverse=True))

	@decorate.record_elapsed_time
	def choose_goal(self, axioms, learned_nodes):	# short sighted, depth-first
		"""
		:returns: One immediate successor to learned_nodes which we should set as the new goal (chosen by depth, then learn count, then importance, then id).
		"""
		self.validate_input_nodes(axioms)
		self.validate_input_nodes(learned_nodes)
		depth_to_successors_dict = self.depth_to_successors_dict(axioms, learned_nodes)
		deepest_successors = list(depth_to_successors_dict.items())[0][1]

		# Now sort the deepest successors by learn count, then by importance, and finally name to break a tie.
		# If we need better efficiency, use DiGraph.learn_counts(targets, learned_nodes)
		def learn_count_sorter(successor):
			return (
				self.learn_count(successor, learned_nodes),
				-self.importance_weight(successor),
				self.n(successor).id,
			)
		goal = sorted(deepest_successors, key=learn_count_sorter)[0]
		return goal

	@decorate.record_elapsed_time
	def learnable_pregoals(self, goal, learned_nodes):	# a pregoal is an unlearned dependency of the goal, or the goal itself
		learnable_nodes = set(self.absolute_dominion(learned_nodes))
		pregoals = self.unlearned_dependency_tree(goal, learned_nodes)
		return set.intersection(learnable_nodes, pregoals)

	@decorate.record_elapsed_time
	def choose_learnable_pregoals(self, axioms, learned_nodes, number=1, goal=None):
		if not goal:
			goal = self.choose_goal(axioms, learned_nodes)
		learnable_pregoals = self.learnable_pregoals(goal, learned_nodes)
		return self.most_important(learnable_pregoals, number)

nx.DAG = _DAG
