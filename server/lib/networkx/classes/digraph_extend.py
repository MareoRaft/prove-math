################################## IMPORTS ####################################
import networkx as nx
from lib import log

from lib.networkx.classes import graph_extend

from warnings import warn

################################## HELPERS ####################################
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
	for dic in list_of_dics:
		if dic['_id'] == ID:
			return dic
	# if the id doesn't exist, make a fake node...
	warn('Could node find dict with ID "' + ID + '" within list_of_dics.')
	return {"_id": ID, "empty": True, "_importance": 4, "_name": ""}

def log_function_call(func):
	def new_func(*args, **kwargs):
		start_time = time.time()
		out = func(*args, **kwargs)
		elapsed_time = time.time() - start_time
		log_msg = time.ctime() + '\tFunction: ' + func.__name__ + '\tRuntime: ' + str(elapsed_time)
		print(log_msg)
#		print("Result:", str(out))
		return out
	return new_func
#################################### MAIN #####################################


class _DiGraphExtended (nx.DiGraph):

	@log.elapsed_time
	def validate(self):
		if not self.is_directed():
			raise TypeError('is_source only accepts DiGraphs as input')
		return True

	@log.elapsed_time
	def predecessor(self, node): # finds any single predecessor of a node in a Directed Graph
		return next(self.predecessors_iter(node), None)

	def successor(self, node): # should follow the same exact pattern as predecessor
		return next(self.successors_iter(node), None)

	def predecessors(self, nbunch):	#works for single or multiple input nodes
		if not self.acceptable_iterable(nbunch):	#single input node
			pred = set(self.predecessors_iter(nbunch))
		else:
			pred = set()
			if len(nbunch) == 0:	#empty iterable
				raise ValueError('Argument {} is empty'.format(str(nbunch)))
			else:	#multiple input nodes
#possibly reimplement for better efficiency
				for node in nbunch:
					pred = pred.union(set(self.predecessors_iter(node)))
		return pred - set(nbunch)

	def successors(self, nbunch):	# should follow the same exact pattern as predecessors
		if not self.acceptable_iterable(nbunch):	#single input node
			succ = set(self.successors_iter(nbunch))
		else:
			succ = set()
			if len(nbunch) == 0:	#empty iterable
				raise ValueError('Argument {} is empty'.format(str(nbunch)))
			else:	#multiple input nodes
#possibly reimplement for better efficiency
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

	def shortest_anydirectional_path(self, source=None, target=None):
		DG = self.to_undirected() # if we need this, we should optimize it.
		return shortest_path_helper(DG, source, target)

	def ancestors(self, nbunch):
		self.validate_input_nodes(nbunch)
		if not self.acceptable_iterable(nbunch):	#single input node
			return nx.ancestors(self, nbunch)
		else:
			if len(nbunch) == 1:	#still a single node
				return nx.ancestors(self, nbunch[0])
			else:	#multiple input nodes
				DG = self.copy()
				t = DG.add_node_unique()
				for node in nbunch:
					DG.add_edge(node, t) # this automatically adds t to DG too
				return nx.ancestors(DG, t) - set(nbunch) # returns a SET

	def common_ancestors(self, nbunchA, nbunchB):
#possibly reimplement for better efficiency
		ancA = self.ancestors(nbunchA)
		ancB = self.ancestors(nbunchB)
		return set.intersection(ancA, ancB)
		
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

	def common_descendants(self, nbunchA, nbunchB):
#possibly reimplement for better efficiency
		descA = self.descendants(nbunchA)
		descB = self.descendants(nbunchB)
		return set.intersection(descA, descB)

	def relatives_to_distance_dict(self, nbunch, cutoff=None):	#name? relatives? relative?
		if not self.acceptable_iterable(nbunch):	#single input node
			source = {nbunch:1}
		else:
			if len(nbunch) == 0:	#empty iterable
				raise ValueError('Argument {} is empty'.format(str(nbunch)))
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
		return seen  # return all path lengths as dictionary

	def descendants_to_distance_dict(self, nbunch, cutoff=None):
		if not self.acceptable_iterable(nbunch):	#single input node
			source = {nbunch:1}
		else:
			if len(nbunch) == 0:	#empty iterable
				raise ValueError('Argument {} is empty'.format(str(nbunch)))
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
			nextlevel = dict.fromkeys(self.successors(thislevel.keys()))
			level += 1
		return seen  # return all path lengths as dictionary

	def as_complete_dict(self):
		graph = dict()
		graph['nodes'] = [self.n(node_id).__dict__ for node_id in self.nodes()]
		graph['links'] = [{'source': source, 'target': target} for (source, target) in self.edges()]
		return graph

	def absolute_dominion(self, nodes): # abs dom of A is A and all nodes absolutely dominated by A (nodes succeeding A and whose predecessors are entirely in A)
		if not self.acceptable_iterable(nodes): #without this, if nodes is just a string, the return statement will not work correctly
			raise ValueError('Argument {} is not iterable'.format(str(nodes)))
		hanging_dominion = self.successors(nodes)
		hanging_absolute_dominion = []
		for candidate in hanging_dominion:
			if set(self.predecessors(candidate)) <= set(nodes):
				hanging_absolute_dominion.append(candidate)
		return hanging_absolute_dominion + list(nodes)

	def unlearned_dependency_tree(self, target, learned_nodes):
		if not self.acceptable_iterable(learned_nodes): #without this, if learned_nodes was a string, then DG.remove_nodes_from(learned_nodes) would cause incorrect behavior
			raise ValueError('Argument {} is not iterable'.format(str(learned_nodes)))
		DG = self.copy()
		DG.remove_nodes_from(learned_nodes)
		return nx.ancestors(DG, target).union({target})

	def learn_count(self, target, learned_nodes):
		return len(self.unlearned_dependency_tree(target, learned_nodes))

	'''
	def learn_counts(self, target_bunch, learned_nodes):
		DG = self.copy()	#lets us bypass calling unlearned_dependency_tree repeatedly
		DG.remove_nodes_from(learned_nodes)
		return [len(DG.ancestors(target)) for target in target_bunch]
	'''
	
	def most_important_weight(self, node):
		distance_from_node = 0
		current_depth_nodes = {node}
		already_counted_nodes = set() #needed in case there are any cycles
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

	def most_important(self, number, nbunch):
		def most_important_sorter(node):
			return (self.most_important_weight(node), self.n(node).id)
		if number <= 0:
			raise ValueError('Must give number > 0')
		if len(nbunch) < number:
			raise ValueError('Asked for more nodes than you provided')
		nodes_by_importance = sorted(nbunch, key=most_important_sorter, reverse=True)
		return nodes_by_importance[:number]

for key, value in _DiGraphExtended.__dict__.items():
	try:
		setattr(nx.DiGraph, key, value)
	except TypeError:
		pass

