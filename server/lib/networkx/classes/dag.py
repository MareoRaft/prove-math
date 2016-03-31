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

	def short_sighted_deepest_successors(self, axioms, learned_nodes):
		distance_dict = self.descendants_to_distance_dict(axioms)
		# nodes that are NOT successors of the axioms will not appear in distance_dict.  This is OK.

### do we want successors = self.successors(learned_nodes) - self.absolute_dominion(learned_nodes)?
###	otherwise we might end up with the "deepest" successor already being dominated by learned_nodes
### in this case learn_count=0 and there is no need to find a source
		successors = self.successors(learned_nodes)
		# now build a reverse dictionary with these...
		distance_to_successors = dict()
		for successor in successors:
			distance_to_successors[distance_dict[successor]] = [] # initialize as array
		for successor in successors:
			distance_to_successors[distance_dict[successor]].append(successor) # actually add the values
	
		return distance_to_successors

	def short_sighted_depth_first_unlearned_source(self, axioms, learned_nodes): # not necessarily a source, as it is
		if learned_nodes not a subset of self.nodes():
			raise Exception('Nodes not part of graph.')
		distance_to_successors = self.short_sighted_deepest_successors(axioms, learned_nodes)
	
		# take the successor w/ minimum learn_count, and IMPORTANCE to break a tie, then ALPHABETICAL
		graph = self
###		#why?
		
		def sorter_learn_count(successor):
			# the keys are ids, so we can get the node...
###			#learn_count is simply len(graph.unlearned_dependency_tree(target, learned_nodes))
			return (len(graph.unlearned_dependency_tree(successor, learned_nodes)), -graph.n(successor).importance, graph.n(successor).id)
	
		def sorter_depth(node):
			return (depth_dict[node.id], node.importance) # or self.n(node).importance

#this line doesn't seem to work:
#		for depth, successors in sorted(distance_to_successors, key=distance_to_successors.get, reverse=True).items():
#sorted(dict, key=dict.get) returns a list not a dict, so it does not have an items() method
#try this:
		for depth, successors in sorted(distance_to_successors.items(), reverse=True)
			for successor in sorted(successors, key=sorter_learn_count):
				unlearned_dependency_tree, depth_dict = self.unlearned_dependency_tree(successor, learned_nodes) # this INCLUDES the successor itself.  Remember, these are UNLEARNED successors
				for guy_to_learn in sorted(depth_dict, key=sorter_depth, reverse=True):
					return guy_to_learn
### rather than for loops is it cleaner to write this as:
		
#		#sorted_distances_successors_tuples = sorted(distance_to_successors.items(), reverse=True)
#		#deepest_successors = sorted_distances_successors_tuples[0][1]
#		#sorted_deepest_successors = sorted(deepest_successors, key=sorter_learn_count)
#		#guy_to_learn = sorted_deepest_successors[0]
#		#prereqs = self.unlearned_dependency_tree(guy_to_learn, learned_nodes)
#		#sorted_prereqs = sorted(prereqs, key=lambda node: self.n(node).importance, reverse=True)
#		#next_target = sorted_prereqs[0]
#		#return next_target

# or instead of doing sorted_prereqs by importance, it would be nice to do it by learn_count
# but that would require running unlearned_dependency_tree on each prereq list item and will make things even slower than they already are
		


	#deepest_successors_dict = dict()
	#for key in short_sighted_deepest_successors:
	#	deepest_successors_dict[key] = self.learn_count(key) # we can make a learn count and sources so that we don't have to re-find the sources later.  this can be a future optimization
	#node = take the min
	## finally, return the sources of our node
	#dep_tree = self.dependency_tree(node)
	#return self.sources(dep_tree)


	# def short_sighted_depth_first_unlearned_source(self, axioms, learned_nodes):
	# 	unlearned_sources = self.short_sighted_depth_first_unlearned_source(axioms, learned_nodes)
	# 	if unlearned_sources:
	# 		return unlearned_sources[0]
	# 	else:
	# 		return None


nx.DAG = _DAG
