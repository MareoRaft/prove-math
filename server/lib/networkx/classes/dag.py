################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import digraph_extend

import json

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

	def short_sighted_deepest_successors(self, axioms, learned_nodes):
		distance_dict = self.multiple_sources_shortest_path_length(axioms)
		# nodes that are NOT successors of the axioms will not appear in distance_dict.  This OK.

		successor_ids = self.hanging_dominion(learned_nodes)
		# now build a reverse dictionary with these...
		distance_to_successor_ids = dict()
		for successor_id in successor_ids:
			distance_to_successor_ids[distance_dict[successor_id]] = [] # initialize as array
		for successor_id in successor_ids:
			distance_to_successor_ids[distance_dict[successor_id]].append(successor_id) # actually add the values

		return distance_to_successor_ids

	def unlearned_dependency_tree(self, node, learned_nodes):
		unlearned_nodes = set(node)
		for predecessor in self.predecessors(node):
			if predecessor is not in learned_nodes:
				unlearned_nodes = unlearned_nodes + self.unlearned_dependency_tree(predecessor)
		return unlearned_nodes

	def short_sighted_depth_first_unlearned_source(self, axioms, learned_node_ids, graph_node_dict): # not necessarily a source, as it is
		if learned_node_ids not a subset of self:
			raise Exception('Nodes not part of graph.')
		distance_to_successor_ids = self.short_sighted_deepest_successors(axioms, learned_node_ids)

		# take the successor w/ minimum learn_count, and IMPORTANCE to break a tie, then ALPHABETICAL
		graph = self
		def sorter_learn_count(successor_id):
			# the keys are ids, so we can get the node...
			return (graph.learn_count(successor_id, learned_node_ids), -graph_node_dict[successor_id].importance)

		def sorter_depth(node_id):
			return (depth_dict[node_id], graph_node_dict[node_id].importance)

		for depth, successor_ids in sorted(distance_to_successor_ids, key=distance_to_successor_ids.get, reverse=True).items():
			for successor_id in sorted(successor_ids, key=sorter_learn_count):
				unlearned_dependency_tree, depth_dict = self.unlearned_dependency_tree(successor_id, learned_node_ids) # this INCLUDES the successor_id itself.  Remember, these are UNLEARNED successor_ids
				for guy_to_learn in sorted(depth_dict, key=sorter_depth, reverse=True):
					return guy_to_learn


		#deepest_successors_dict = dict()
		#for key in short_sighted_deepest_successors:
		#	deepest_successors_dict[key] = self.learn_count(key) # we can make a learn count and sources so that we don't have to re-find the sources later.  this can be a future optimization
		#node = take the min
		## finally, return the sources of our node
		#dep_tree = self.dependency_tree(node)
		#return self.sources(dep_tree)


	# def short_sighted_depth_first_unlearned_source(self, axioms, learned_node_ids, graph_node_dict):
	# 	unlearned_sources = self.short_sighted_depth_first_unlearned_source(axioms, learned_node_ids)
	# 	if unlearned_sources:
	# 		return unlearned_sources[0]
	# 	else:
	# 		return None


nx.DAG = _DAG
