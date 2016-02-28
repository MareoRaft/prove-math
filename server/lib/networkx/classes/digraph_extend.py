################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import graph_extend

from warnings import warn

################################## HELPERS ####################################
def create_s_pointing_to_source(DG, source):
	if not hasattr(source, '__iter__'): # although strings are iterable, they don't have __iter__.  My goal is that "scalar" values will get stuffed into a list.  But lists and sets will not.
		source = [source]
	s = DG.add_node_unique()
	for node in source:
		DG.add_edge(s, node) # this automatically adds s to G too
	return s

def create_t_pointing_from_target(DG, target):
	if not hasattr(target, '__iter__'):
		target = [target]
	t = DG.add_node_unique()
	for node in target:
		DG.add_edge(node, t)
	return t

def shortest_path_helper(DG, source, target): # the REASON why this function is NEEDED is because it allows "source" and "target" to be SETS (or any iterables) of nodes.  This enables our shortest path function to find the shortest path between any two SETS of nodes! :)
	s = create_s_pointing_to_source(DG, source)
	t = create_t_pointing_from_target(DG, target)

	try:
		return nx.shortest_path(DG, source=s, target=t)[1:-1] # the final 1:-1 cuts off the first and last element, that is, s and t.
	except nx.exception.NetworkXNoPath:
		return None

def find_dict_from_id(list_of_dics, ID):
	for dic in list_of_dics:
		if dic['_id'] == ID:
			return dic
	# if the id doesn't exist, make a fake node...
	warn('Could node find dict with ID "' + ID + '" within list_of_dics.')
	return {"_id": ID, "empty": True, "_importance": 4, "_name": ""}

#################################### MAIN #####################################


class _DiGraphExtended (nx.DiGraph):


	def validate(self):
		if not self.is_directed():
			raise TypeError('is_source only accepts DiGraphs as input')
		return True

	def predecessor(self, node): # finds any predecessor of a node in a Directed Graph (in the future this should NOT depend on DG.predecessors(node), but instead re-implement the code of .predecessors and stop after finding 1)
		ps = self.predecessors(node)
		if ps:
			return ps[0]
		else:
			return None

	def successor(self, node): # should follow the same exact pattern as predecessor
		ss = self.successors(node)
		if ss:
			return ss[0]
		else:
			return None

	def is_source(self, node): # checks if a node is a source of a Directed Graph
		return self.predecessor(node) == None

	def shortest_path(self, source=None, target=None): # since this is a DiGraph obj, this gives the shortest DIRECTED path
		DG = self.copy()
		return shortest_path_helper(DG, source, target)

	def shortest_anydirectional_path(self, source=None, target=None):
		DG = self.to_undirected() # if we need this, we should optimize it.
		return shortest_path_helper(DG, source, target)

	def ancestors(self, nbunch):
		return nx.ancestors(self, nbunch) # returns a SET

	def descendants(self, nbunch):
		return nx.descendants(self, nbunch)

	def common_descendants(self, nbunchA, nbunchB):
		descA = self.descendants(nbunchA)
		descB = self.descendants(nbunchB)
		return set.intersection(descA, descB)

	def single_source_shortest_anydirectional_path_length(self, source, cutoff=None):
		 seen={}                  # level (number of hops) when seen in BFS
		 level=0                  # the current level
		 nextlevel={source:1}  # dict of nodes to check at next level
		 while nextlevel:
			 thislevel=nextlevel  # advance to next level
			 nextlevel={}         # and start a new list (fringe)
			 for v in thislevel:
				 if v not in seen:
					 seen[v]=level # set the level of vertex v
					 neighbors=nx.all_neighbors(self,v)
					 nextlevel.update(dict.fromkeys(neighbors)) # add neighbors of v
			 if (cutoff is not None and cutoff <= level):  break
			 level=level+1
		 return seen  # return all path lengths as dictionary

	def multiple_sources_shortest_path_length(self, sources, cutoff=None):
		 seen={}                  # level (number of hops) when seen in BFS
		 level=0                  # the current level
		 nextlevel={}  # dict of nodes to check at next level
		 for source in sources:
		 	nextlevel[source] = 1
		 while nextlevel:
			 thislevel=nextlevel  # advance to next level
			 nextlevel={}         # and start a new list (fringe)
			 for v in thislevel:
				 if v not in seen:
					 seen[v]=level # set the level of vertex v
					 nextlevel.update(self[v]) # add neighbors of v
			 if (cutoff is not None and cutoff <= level):  break
			 level=level+1
		 return seen  # return all path lengths as dictionary

	def as_complete_dict(self):
		graph = dict()
		graph['nodes'] = [self.n(node_id).__dict__ for node_id in self.nodes()]
		graph['links'] = [{'source': source, 'target': target} for (source, target) in self.edges()]
		return graph

	def hanging_dominion(self, nodes):
		hanging_dominion_and_extra = set()
		for node in nodes:
			hanging_dominion_and_extra = hanging_dominion_and_extra.union(set(self.successors(node)))
		return hanging_dominion_and_extra - set(nodes)

	def absolute_dominion(self, nodes): # abs dom of A is A and all nodes absolutely dominated by A (nodes succeeding A and whose predecessors are entirely in A)
		hanging_dominion = self.hanging_dominion(nodes)
		hanging_absolute_dominion = []
		for candidate in hanging_dominion:
			if set(self.predecessors(candidate)) <= set(nodes):
				hanging_absolute_dominion.append(candidate)
		return hanging_absolute_dominion + nodes

	def common_ancestors(self, nbunchA, nbunchB):
		return set.intersection(self.ancestors(nbunchA), self.ancestors(nbunchB))

	def most_important(self, number, nodes):
		if number <= 0:
			raise ValueError('Must give number > 0')
		if len(nodes) < number:
			return nodes
			#or raise ValueError('Must provide at least <number> nodes')?
		else:
			#sort nodes by importance and return the first <number> of them
			important_nodes = sorted(nodes, key=lambda node: -1*(self.n(node).importance))
			return important_nodes[:number]
				

	def unlearned_dependency_tree(self, target, learned_nodes):
		dependencies = self.ancestors(target)
		return dependencies - set(learned_nodes)

for key, value in _DiGraphExtended.__dict__.items():
	try:
		setattr(nx.DiGraph, key, value)
	except TypeError:
		pass

