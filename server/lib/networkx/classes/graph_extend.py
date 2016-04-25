################################## IMPORTS ####################################
import time
from warnings import warn

import networkx as nx

################################## HELPERS ####################################
def string_unique():
	return str(time.time())

#################################### MAIN #####################################


class _GraphExtended (nx.Graph):

	ACCEPTABLE_ITERABLES = [list, set, type(dict().keys())]	#dict, nx.Graph later

	def acceptable_iterable(self, nbunch):
		return type(nbunch) in self.ACCEPTABLE_ITERABLES

	def is_nonnull(self):
		return bool(self.nodes())

	def is_null(self):
		return not self.is_nonnull()

	def add_node_unique(self):
		while True:
			n = 'node_unique.' + string_unique()
			if self.has_node(n):
				warn('The node already existed.')
				continue
			else:
				self.add_node(n)
				break
		return n

	def n(self, node_id):
		return self.node[node_id]["custom_object"]

	def add_n(self, nodebunch):
		if not self.acceptable_iterable(nodebunch): # nodebunch must be a single node
			nodebunch = [nodebunch]
		for node in nodebunch:
			self.add_node(node.id, attr_dict={"custom_object": node})

	def validate_input_nodes(self, nbunch):
		#checks that all given inputs exist in the graph
		if not self.acceptable_iterable(nbunch):
			nbunch = [nbunch]
		if len(nbunch) == 0:	#empty iterable
			raise ValueError('Argument {} is empty'.format(str(nbunch)))
		elif len(nbunch) == 1:	#single node
			if not self.has_node(nbunch[0]):
				raise nx.NetworkXError('The input node {} is not in the graph'.format(str(nbunch[0])))
			return True
		else:	#multiple nodes
			for node in nbunch:
				if not self.has_node(node):
					raise nx.NetworkXError('One of the listed nodes is not in the graph')
			return True


for key, value in _GraphExtended.__dict__.items():
	try:
		setattr(nx.Graph, key, value)
	except TypeError:
		pass
