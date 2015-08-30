################################## IMPORTS ####################################
import networkx as nx

from lib.networkx.classes import digraph_extend

from warnings import warn
import json

################################# HELPERS #####################################
def find_dict_from_id(list_of_dics, ID):
	for dic in list_of_dics:
		if dic['_id'] == ID:
			return dic
	# if the id doesn't exist, make a fake node...
	warn('Could node find dict with ID "' + ID + '" within list_of_dics.')
	return {"_id": ID, "empty": True, "_importance": 4, "_name": ""}

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

	def as_complete_dict(self, list_of_complete_nodes):
		graph = dict()
		graph['nodes'] = [find_dict_from_id(list_of_complete_nodes, dict_id) for dict_id in self.nodes()]
		graph['links'] = [{'source': source, 'target': target} for (source, target) in self.edges()]
		return graph

	def as_complete_json(self, list_of_complete_nodes):
		graph_dict = self.as_complete_dict(list_of_complete_nodes)
		return json.dumps(graph_dict) # for the future, the following may be faster: 1. simplejason or 2. cjson


nx.DAG = _DAG

