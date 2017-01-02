############################ IMPORTS #############################
import json
from collections import OrderedDict

import networkx as nx
from lib.networkx.classes import digraph_extend

from lib.decorate import record_elapsed_time
from lib import helper

########################### HELPERS #############################

############################# MAIN #############################


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

	def common_descendant_sources(self, nbunchA, nbunchB):
		return self.subgraph(self.common_descendants(nbunchA, nbunchB)).sources()

	def has_path(self, start, end):
		return nx.has_path(self, start, end)

	# @record_elapsed_time
	def remove_redundant_edges(self): # We need to be careful not to perform this on a live graph, since it temporarily alters the graph.
		for edge in self.edges():
			self.remove_edge(edge[0], edge[1])
			if not self.has_path(edge[0], edge[1]):
				self.add_edge(edge[0], edge[1])

	# @record_elapsed_time
	def depth_to_successors_dict(self, axioms, learned_nodes):	# short sighted
		"""
		:param acceptable_iter axioms: The "bottom" of our graph.  The distance from the axioms is the depth.
		:returns: A dictionary where the keys are depths (ordered greatest to least), values are lists of successors sharing that depth.
		:rtype: OrderedDict

		*Note: nodes that are NOT descendants of the axioms will not appear in the dictionary.  This is OK.
		"""
		descendants_to_distance_dict = self.descendants_to_distance_dict(axioms)
		successors = self.successors(learned_nodes)
		successors_to_distance_dict = {k:v for k,v in descendants_to_distance_dict.items() if k in successors}
		depth_to_successors_dict = helper.reversed_dict(successors_to_distance_dict)
		return OrderedDict(sorted(depth_to_successors_dict.items(), key=lambda t: t[0], reverse=True))

nx.DAG = _DAG
