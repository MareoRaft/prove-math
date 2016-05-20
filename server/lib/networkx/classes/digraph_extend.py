########################### IMPORTS #############################
import networkx as nx
from warnings import warn

from lib.decorate import record_elapsed_time
from lib.networkx.classes import graph_extend

########################### HELPERS #############################
def create_s_pointing_to_source(DG, source):
	if not DG.acceptable_iterable(source): # My goal is that "scalar" values will get stuffed into a list.  But lists and sets will not.
		source = [source]
	s = DG.add_node_unique()
	for node in source:
		DG.add_edge(s, node) # this automatically adds s to G too
	return s

def create_t_pointing_from_target(DG, target):
	if not DG.acceptable_iterable(target):
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
	""" WARNING.  If you are using this function, you are probably not doing things in the most efficient way.  This is only here just in case we need it.
	"""
	for dic in list_of_dics:
		if dic['_id'] == ID:
			return dic
	# if the id doesn't exist, make a fake node...
	warn('Could node find dict with ID "' + ID + '" within list_of_dics.')
	return {"_id": ID, "empty": True, "_importance": 4, "_name": ""}

############################## MAIN ##############################


class _DiGraphExtended (nx.DiGraph):

	def validate(self):
		if not self.is_directed():
			raise TypeError('is_source only accepts DiGraphs as input')
		return True

	def predecessor(self, node): # finds any single predecessor of a node in a Directed Graph
		return next(self.predecessors_iter(node), None)

	def successor(self, node): # should follow the same exact pattern as predecessor
		return next(self.successors_iter(node), None)

	@record_elapsed_time
	def predecessors(self, nbunch):	# works for single or multiple input nodes
		if not self.acceptable_iterable(nbunch):	# single input node
			pred = set(self.predecessors_iter(nbunch))
		else:
			pred = set()
			if len(nbunch) == 0:	# empty iterable
				raise ValueError('Argument {} is empty'.format(nbunch))
			else:	# multiple input nodes
				for node in nbunch:
					pred = pred.union(set(self.predecessors_iter(node)))
		return pred - set(nbunch)

	@record_elapsed_time
	def successors(self, nbunch):	# should follow the same exact pattern as predecessors
		if not self.acceptable_iterable(nbunch):
			succ = set(self.successors_iter(nbunch))
		else:
			succ = set()
			if len(nbunch) == 0:
				raise ValueError('Argument {} is empty'.format(nbunch))
			else:
				for node in nbunch:
					succ = succ.union(set(self.successors_iter(node)))
		return succ - set(nbunch)

	def anydirectional_neighbors(self, nbunch):
		return set.union(self.predecessors(nbunch), self.successors(nbunch))

	def is_source(self, node): # checks if a node is a source of a Directed Graph
		return self.predecessor(node) == None

	def shortest_path(self, source=None, target=None): # since this is a DiGraph obj, this gives the shortest DIRECTED path
		DG = self.copy()
		return shortest_path_helper(DG, source, target)

	@record_elapsed_time
	def shortest_anydirectional_path(self, source=None, target=None):
		DG = self.to_undirected() # if we need this, we should optimize it.
		return shortest_path_helper(DG, source, target)

	@record_elapsed_time
	def ancestors(self, nbunch):
		self.validate_input_nodes(nbunch)
		if not self.acceptable_iterable(nbunch):	# single input node
			return nx.ancestors(self, nbunch)
		else:
			if len(nbunch) == 1:	# still a single node
				return nx.ancestors(self, nbunch[0])
			else:	# multiple input nodes
				DG = self.copy()
				t = DG.add_node_unique()
				for node in nbunch:
					DG.add_edge(node, t) # this automatically adds t to DG too
				return nx.ancestors(DG, t) - set(nbunch) # returns a SET

	@record_elapsed_time
	def common_ancestors(self, nbunchA, nbunchB):
		ancA = self.ancestors(nbunchA)
		ancB = self.ancestors(nbunchB)
		return set.intersection(ancA, ancB)

	@record_elapsed_time
	def descendants(self, nbunch):
		self.validate_input_nodes(nbunch)
		if not self.acceptable_iterable(nbunch):	#single input node
			return nx.descendants(self, nbunch)
		else:
			if len(nbunch) == 1:	#still a single node
				return nx.descendants(self, nbunch[0])
			else:	#multiple input nodes
				DG = self.copy()
				s = DG.add_node_unique()
				for node in nbunch:
					DG.add_edge(s, node) # this automatically adds s to DG too
				return nx.descendants(DG, s) - set(nbunch) # returns a SET

	@record_elapsed_time
	def common_descendants(self, nbunchA, nbunchB):
		descA = self.descendants(nbunchA)
		descB = self.descendants(nbunchB)
		return set.intersection(descA, descB)

	@record_elapsed_time
	def relatives_to_distance_dict(self, nbunch, cutoff=None):
		"""
		:param int cutoff: Maximum distance to search for.
		:returns: A dictionary where the nodes (relatives) are keys and shortest path lengths (distance) are values.
		:rtype: dict
		"""
		if not self.acceptable_iterable(nbunch):	# single input node
			source = {nbunch:1}
		else:
			if len(nbunch) == 0:	# empty iterable
				raise ValueError('Argument {} is empty'.format(nbunch))
			else:
				source = {}
				for node in nbunch:
					source[node] = 1
		seen = {}                  # level (number of hops) when seen in BFS
		level = 0                  # the current level
		nextlevel = source  # set of nodes to check at next level
		while nextlevel:
			thislevel = nextlevel  # advance to next level
			for v in thislevel:
				if v not in seen:
					seen[v] = level # set the level of vertex v
			if (cutoff is not None and cutoff <= level):  break
			nextlevel = dict.fromkeys(self.anydirectional_neighbors(thislevel.keys()))
			level += 1
		return seen

	@record_elapsed_time
	def descendants_to_distance_dict(self, nbunch, cutoff=None):
		""" Same as relatives_to_distance_dict, but only descendants of the nbunch. """
		if not self.acceptable_iterable(nbunch):
			source = {nbunch:1}
		else:
			if len(nbunch) == 0:
				raise ValueError('Argument {} is empty'.format(nbunch))
			else:
				source = {}
				for node in nbunch:
					source[node] = 1
		seen = {}
		level = 0
		nextlevel = source
		while nextlevel:
			thislevel = nextlevel
			for v in thislevel:
				if v not in seen:
					seen[v] = level
			if (cutoff is not None and cutoff <= level):  break
			nextlevel = dict.fromkeys(self.successors(thislevel.keys()))
			level += 1
		return seen

	@record_elapsed_time
	def absolute_dominion(self, nodes): # abs dom of A is A and all nodes absolutely dominated by A (nodes succeeding A and whose predecessors are entirely in A)
		if not self.acceptable_iterable(nodes): #without this, if nodes is just a string, the return statement will not work correctly
			raise ValueError('Argument {} is not iterable'.format(nodes))
		successors = self.successors(nodes)
		hanging_absolute_dominion = []
		for candidate in successors:
			if set(self.predecessors(candidate)) <= set(nodes):
				hanging_absolute_dominion.append(candidate)
		return hanging_absolute_dominion + list(nodes)

for key, value in _DiGraphExtended.__dict__.items():
	try:
		setattr(nx.DiGraph, key, value)
	except TypeError:
		pass

