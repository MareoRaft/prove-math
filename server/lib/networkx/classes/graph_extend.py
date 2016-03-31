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

	def add_n(self, node):
		self.add_node(node.id, attr_dict={"custom_object": node})
	
	def acceptable_iterable(self, nbunch):
		return type(nbunch) in self.ACCEPTABLE_ITERABLES

for key, value in _GraphExtended.__dict__.items():
	try:
		setattr(nx.Graph, key, value)
	except TypeError:
		pass
