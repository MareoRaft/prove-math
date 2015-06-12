#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

################################## HELPERS ####################################
import time

def string_unique():
	return str(time.time())

def create_s_pointing_to_source(DG, source):
	if not hasattr(source, '__iter__'): # although strings are iterable, they don't have __iter__.  My goal is that "scalar" values will get stuffed into a list.  But lists and sets will not.
		source = [source]
	s = 'temporary_node.s.' + string_unique() # this node is meant to be unique from everything else in the graph
	for node in source:
		DG.add_edge(s, node) # this automatically adds s to G too
	return s

def create_t_pointing_from_target(DG, target):
	if not hasattr(target, '__iter__'):
		target = [target]
	t = 'temporary_node.t.' + string_unique()
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

#################################### MAIN #####################################
import networkx as nx
import graph_extend

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
		DG = self.to_undirected()
		return shortest_path_helper(DG, source, target)

	def ancestors(self, nbunch):
		return nx.ancestors(self, nbunch) # returns a SET

	def descendants(self, nbunch):
		return nx.descendants(self, nbunch)

	def common_descendants(self, nbunchA, nbunchB):
		descA = self.descendants(nbunchA)
		descB = self.descendants(nbunchB)
		return set.intersection(descA, descB)

for key, value in _DiGraphExtended.__dict__.items():
	try:
		setattr(nx.DiGraph, key, value)
	except TypeError:
		pass


