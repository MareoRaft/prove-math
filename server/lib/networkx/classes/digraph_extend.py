################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import graph_extend

from warnings import warn

################################## HELPERS ####################################
def create_s_pointing_to_source(DG, source):
	#This line originally took advantage of the '__iter__' attribute, which lists and sets have but lists do not
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

def shortest_path_helper(DG, source, target):
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
		if not self.acceptable_iterable(nbunch):	#single input node
			return nx.ancestors(self, nbunch)
		else:
			if len(nbunch) == 0:	#empty iterable
				raise ValueError('Argument {} is empty'.format(str(nbunch)))
			elif len(nbunch) == 1:	#still a single node
				return nx.ancestors(self, nbunch[0])
			else:	#multiple input nodes
				#make sure all the nodes exist:
				if False in [self.has_node(node) for node in nbunch]:
					raise nx.NetworkXError('One of the listed nodes is not in the graph')
				DG = self.copy()
				t = DG.add_node_unique()
				for node in nbunch:
					DG.add_edge(node, t) # this automatically adds t to DG too
				return nx.ancestors(DG, t) - set(nbunch) # returns a SET

	def common_ancestors(self, nbunchA, nbunchB):
		#possibly reimplement for better efficiency
		return set.intersection(self.ancestors(nbunchA), self.ancestors(nbunchB))
		
	def descendants(self, nbunch):
		if not self.acceptable_iterable(nbunch):	#single input node
			return nx.descendants(self, nbunch)
		else:
			if len(nbunch) == 1:	#still a single node
				return nx.descendants(self, nbunch[0])
			elif len(nbunch) == 0:	#empty iterable
				raise ValueError('Argument {} is empty'.format(str(nbunch)))
			else:	#multiple input nodes
				#make sure all the nodes exist:
				if False in [self.has_node(node) for node in nbunch]:
					raise nx.NetworkXError('One of the listed nodes is not in the graph')
				DG = self.copy()
				s = DG.add_node_unique()
				for node in nbunch:
					DG.add_edge(s, node) # this automatically adds t to DG too
				return nx.descendants(DG, s) - set(nbunch) # returns a SET

	def common_descendants(self, nbunchA, nbunchB):
		#possibly reimplement for better efficiency
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

	def unlearned_dependency_tree(self, target, learned_nodes):
		DG = self.copy()
		DG.remove_nodes_from(learned_nodes)
		return nx.ancestors(DG, target)

	def get_all_successors(self, nbunch):	#works for multiple input nodes
		#inefficient, can make a copy and remove nodes in succ as we go along
		succ = set()
		for node in nbunch:
			succ = set.union(succ, set(self.successors(node)))
		return succ

	def get_all_predecessors(self, nbunch):	#works for multiple input nodes
		#inefficient, can make a copy and remove nodes in pred as we go along
		pred = set()
		for node in nbunch:
			pred = set.union(pred, set(self.predecessors(node)))
		return pred

	def get_all_neighbors(self, nbunch):
		return set.union(self.get_all_successors(nbunch), self.get_all_predecessors(nbunch))
		
	def most_important(self, number, nbunch):
		#note - there might be a way more efficient way to do this, since using a sorting key
		#calls the weight function on every node, whereas it is only necessary to sort nodes with the same importance
		def most_important_weight(node):
			# return (self.n(node).importance, 0, self.n(node).id)
			distance_from_node = 0
			current_depth_nodes = {node}
			already_counted_nodes = {node} #needed in case there are any cycles
#			successors = {node}
#			predecessors = {node}
			avg_importances = [] #average of the nodes in each depth level
			while distance_from_node < 2:
				distance_from_node += 1
#				successors = self.get_all_successors(successors)
#				predecessors = self.get_all_predecessors(predecessors)
#				current_depth_nodes = set.union(successors, predecessors)
				current_depth_nodes = self.get_all_neighbors(current_depth_nodes) - already_counted_nodes	#needed in case there are any cycles
				if len(current_depth_nodes) == 0:	#no more neighbors, don't look any further
					avg_importances.append(0)
#					print("\nFound no neighbors\n")
					break
				current_importances = [self.n(n).importance for n in current_depth_nodes]
#				print("\nNode:", node, "current_depth_nodes:", current_depth_nodes, "current_importances:", current_importances, sep=" ")
				current_avg = sum(current_importances) / len(current_importances)
				avg_importances.append(current_avg)
				already_counted_nodes = set.union(already_counted_nodes, current_depth_nodes)
			weighted_avgs = [(avg/(index+1)**2) for index, avg in enumerate(avg_importances)]	#average of the nodes in each depth level, weighted against distance from node
			neighbors_weight = sum(weighted_avgs)
#			print("Node:", str(node), "importance:", self.n(node).importance, "neighbors_weight:", neighbors_weight, "unweighted_avgs", avg_importances, "weighted avgs", weighted_avgs, sep=" ")
			return (self.n(node).importance, neighbors_weight, self.n(node).id)
		
		if number <= 0:
			raise ValueError('Must give number > 0')
		if len(nbunch) < number:
			raise ValueError('Asked for more nodes than you provided')
		nodes_by_importance = sorted(nbunch, key=most_important_weight, reverse=True)
		return nodes_by_importance[:number]

for key, value in _DiGraphExtended.__dict__.items():
	try:
		setattr(nx.DiGraph, key, value)
	except TypeError:
		pass

