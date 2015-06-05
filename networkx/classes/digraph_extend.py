#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')
###############################################################################

import networkx as nx

class DiGraph (nx.DiGraph):
	def validate(self):
		if not self.is_directed():
			raise TypeError('is_source only accepts DiGraphs as input')
		return True

	def predecessor(self, node): # finds any predecessor of a node in a Directed Graph (in the future this should NOT depend on DG.predecessors(node), but instead re-implement the code of .predecessors and stop after finding 1)
		return self.predecessors(node)[0]

	def successor(self, node): # should follow the same exact pattern as predecessor
		return self.successors(node)[0]

	def is_source(self, node): # checks if a node is a source of a Directed Graph
		return self.predecessor() == None

	def shortest_anydirectional_path(self, source=None, target=None):
		G = self.to_undirected()
		return self.shortest_path(source=source, target=target)

	def common_descendants(self, nbunchA, nbunchB):
		descA = self.descendants(nbunchA)
		descB = self.descendants(nbunchB)
		return list(set.intersection(set(descA), set(descB)))




nx.DiGraph = DiGraph


G = nx.DiGraph()
print(G.validate())

