################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import digraph_extend
from collections import OrderedDict

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

	def short_sighted_depth_to_successors_dict(self, axioms, learned_nodes):
		#returns an ORDERED dict where the keys are depths (ordered greatest to least), values are lists of successors sharing that depth
		# nodes that are NOT descendants of the axioms will not appear in distance_dict.  This is OK.
		distance_dict = self.descendants_to_distance_dict(axioms)
		successors = self.successors(learned_nodes)
		# now build a reverse dictionary with these...
		depth_to_successors_dict = OrderedDict()
		for depth in sorted(distance_dict.values(), reverse=True):
			depth_to_successors_dict[depth] = [] # initialize as array
		for successor in successors:
			depth_to_successors_dict[distance_dict[successor]].append(successor) # actually add the values
		#need to remove empty lists from the dictionary
		for depth, nbunch in depth_to_successors_dict.items():
			if nbunch == []:
				depth_to_successors_dict.pop(depth)
		return depth_to_successors_dict

	def short_sighted_depth_first_choose_goal(self, axioms, learned_nodes):
		#returns one immediate successor to learned_nodes which we should set as the new goal, chosen by depth, then learn count, then importance, then name
		self.validate_input_nodes(axioms) #do we need this?
		self.validate_input_nodes(learned_nodes)
		depth_to_successors_dict = self.short_sighted_depth_to_successors_dict(axioms, learned_nodes)
		deepest_successors = list(depth_to_successors_dict.items())[0][1]

###	or, use this if we actually want to make short_sighted_deepest_successors_dict() return a NON-ordered dict
###		sorted_depths = sorted(depth_to_successors_dict.keys(), reverse=True)
###		deepest_successors = depth_to_successors_dict[sorted_depths[0]]
		
		#now sort the deepest successors by learn count, then by importance, and finally name to break a tie
		if len(deepest_successors) == 1:
#We can easily get rid of this check
#Skipping this will just cause learn_count_sorter to run unnecessarily one time, but this is negligable
			goal = deepest_successors[0]
		else:
#if we need better efficiency consider creating DiGraph.learn_counts(targets, learned_nodes)
			def learn_count_sorter(successor):
				return (self.learn_count(successor, learned_nodes), -self.most_important_weight(successor), self.n(successor).id)
			goal = sorted(deepest_successors, key=learn_count_sorter)[0]
		return goal

	def learnable_prereqs(self, goal, learned_nodes):
		learnable_nodes = set(self.absolute_dominion(learned_nodes))
		prereqs = self.unlearned_dependency_tree(goal, learned_nodes)
		return set.intersection(learnable_nodes, prereqs)

	def choose_next_prereq(self, prereqs, learned_nodes): #choose one from learnable_prereqs
		#sort by learn count, then by importance, then by name
		def learn_count_sorter(prereq):
			return (self.learn_count(prereq, learned_nodes), -self.most_important_weight(prereq), self.n(prereq).id)
		sorted_prereqs = sorted(prereqs, key=learn_count_sorter)
		return sorted_prereqs[0]
#technically this calls learn_count_sorter unnecessarily for the case where prereqs only has a single element, but this inefficiency is totally negligable

	def user_learn_suggestion(self, axioms, learned_nodes, goal=None):
		if not goal:
			goal = self.short_sighted_depth_first_choose_goal(axioms, learned_nodes)
		learnable_prereqs = self.learnable_prereqs(goal, learned_nodes)
		return self.choose_next_prereq(learnable_prereqs, learned_nodes)
			

'''	def short_sighted_depth_first_unlearned_source(self, axioms, learned_nodes): # not necessarily a source, as it is
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
'''

nx.DAG = _DAG
