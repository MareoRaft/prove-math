#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')
###############################################################################

import networkx as nx

def predecessor(DG, node): # finds any predecessor of a node in a Directed Graph (in the future this should NOT depend on DG.predecessors(node), but instead re-implement the code of .predecessors and stop after finding 1)
	if not nx.is_directed(DG):
		raise TypeError('is_source only accepts DiGraphs as input') # Exceptions are general. Exception >= StandardError >= TypeError
	return DG.predecessors(node)[0]

def successor(DG, node): # should follow the same exact pattern as predecessor
	if not nx.is_directed(DG):
		raise TypeError('is_source only accepts DiGraphs as input')
	return DG.successors(node)[0]

def is_source(DG, node): # checks if a node is a source of a Directed Graph
	if not nx.is_directed(DG):
		raise TypeError('is_source only accepts DiGraphs as input')
	return nx.predecessor() == None

def shortest_anydirectional_path(DG, source=None, target=None):
	if not nx.is_directed(DG):
		raise TypeError('shortest_anydirectional_path is for DiGraphs only')
	G = DG.to_undirected()
	return nx.shortest_path(G, source=source, target=target)

def common_descendants(DG, nbunchA, nbunchB):
	if not nx.is_directed(DG):
		raise TypeError('common_descendants is for DiGraphs only')
	descA = nx.descendants(DG, nbunchA)
	descB = nx.descendants(DG, nbunchB)
	return list(set.intersection(set(descA), set(descB)))
