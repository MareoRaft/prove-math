################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import digraph_extend

import json

################################# HELPERS #####################################

#################################### MAIN #####################################


class _DAG (nx.DiGraph):


	def validate(self, error_message=None):
		if not nx.is_directed_acyclic_graph(self):
			raise TypeError('Not a Directed A(dir)cyclcic Graph! ' + str(error_message))
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

	#def short_sighted_deepest_successors(self, axioms, learned_nodes):
	#	distance_dict = self.multiple_sources_shortest_path_length(axioms)
	#	# nodes that are NOT successors of the axioms will not appear in distance_dict.  This is OK.

	#	successors = self.hanging_dominion(learned_nodes)
	#	# now build a reverse dictionary with these...
	#	distance_to_successors = dict()
	#	for successor in successors:
	#		distance_to_successors[distance_dict[successor]] = [] # initialize as array
	#	for successor in successors:
	#		distance_to_successors[distance_dict[successor]].append(successor) # actually add the values

	#	return distance_to_successors

	#def unlearned_dependency_tree(self, node, learned_nodes):
	#	unlearned_nodes = set(node)
	#	for predecessor in self.predecessors(node):
	#		if predecessor not in learned_nodes:
	#			unlearned_nodes = unlearned_nodes + self.unlearned_dependency_tree(predecessor)
	#	return unlearned_nodes

	#def short_sighted_depth_first_unlearned_source(self, axioms, learned_nodes): # not necessarily a source, as it is
	#	if learned_nodes not a subset of self.nodes():
	#		raise Exception('Nodes not part of graph.')
	#	distance_to_successors = self.short_sighted_deepest_successors(axioms, learned_nodes)

	#	# take the successor w/ minimum learn_count, and IMPORTANCE to break a tie, then ALPHABETICAL
	#	graph = self
	#	def sorter_learn_count(successor):
	#		# the keys are ids, so we can get the node...
	#		return (graph.learn_count(successor, learned_nodes), -successor.importance) # or -self.n(successor).importance

	#	def sorter_depth(node):
	#		return (depth_dict[node.id], node.importance) # or self.n(node).importance

	#	for depth, successors in sorted(distance_to_successors, key=distance_to_successors.get, reverse=True).items():
	#		for successor in sorted(successors, key=sorter_learn_count):
	#			unlearned_dependency_tree, depth_dict = self.unlearned_dependency_tree(successor, learned_nodes) # this INCLUDES the successor itself.  Remember, these are UNLEARNED successors
	#			for guy_to_learn in sorted(depth_dict, key=sorter_depth, reverse=True):
	#				return guy_to_learn


	#	#deepest_successors_dict = dict()
	#	#for key in short_sighted_deepest_successors:
	#	#	deepest_successors_dict[key] = self.learn_count(key) # we can make a learn count and sources so that we don't have to re-find the sources later.  this can be a future optimization
	#	#node = take the min
	#	## finally, return the sources of our node
	#	#dep_tree = self.dependency_tree(node)
	#	#return self.sources(dep_tree)


	# def short_sighted_depth_first_unlearned_source(self, axioms, learned_nodes):
	# 	unlearned_sources = self.short_sighted_depth_first_unlearned_source(axioms, learned_nodes)
	# 	if unlearned_sources:
	# 		return unlearned_sources[0]
	# 	else:
	# 		return None


nx.DAG = _DAG
