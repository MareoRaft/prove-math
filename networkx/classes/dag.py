#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')
###############################################################################

import networkx as nx

class DAG (nx.DiGraph):
	def validate(self):
		if not nx.is_directed_acyclic_graph(self):
			raise TypeError('find_source only accepts Directed A(dir)cyclcic Graphs as input')
		return True

	def source(self): # finds any source in Directed A(dir)cyclic Graph
		currentNode = self.nodes[0]
		while( not self.is_source(currentNode) ):
			currentNode = self.predecessor(currentNode)
		return currentNode

	def sources(self): # finds the sources in a Directed A(dir)cyclic Graph
		dag2 = self.copy()
		sources = []
		while(dag2.nonempty()):
			source = source(dag2)
			sources.push(source)
			sourceAndDescendants = {source} | set(source.descendants)
			dag2 = dag2.subgraph( set(dag2.nodes) - sourceAndDescendants )
		return sources

	def common_descendant_sources(self, nbunchA, nbunchB):
		return sources( self.subgraph(common_descendants(DAG, nbunchA, nbunchB)) )


nx.DAG = DAG
