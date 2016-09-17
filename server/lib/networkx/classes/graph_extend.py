############################ IMPORTS #############################
import time
from warnings import warn

import networkx as nx

from lib.node import Node

############################ HELPERS #############################
def string_unique():
	# this could be improved.  it should guarantee to create a unique string.
	return str(time.time())

############################## MAIN ##############################


class _GraphExtended (nx.Graph):


	ACCEPTABLE_ITERABLES = [list, set, type(dict().keys())]	# dict, nx.Graph later

	def acceptable_iterable(self, nbunch):
		for it_type in self.ACCEPTABLE_ITERABLES:
			if isinstance(nbunch, it_type):
				return True
		return False

	def is_nonnull(self):
		return bool(self.nodes())

	def is_null(self):
		return not self.is_nonnull()

	#PM specific
	def n(self, node_id):
		return self.node[node_id]["custom_object"]

	#PM specific
	def add_n(self, nodebunch):
		if not self.acceptable_iterable(nodebunch): # nodebunch must be a single node
			nodebunch = [nodebunch]
		for node in nodebunch:
			self.add_node(node.id, attr_dict={"custom_object": node})

	def add_node_unique(self):
		while True:
			n_id = 'node_unique.' + string_unique()
			if self.has_node(n_id):
				warn('The node already existed.')
				continue
			else:
				node = Node({"name":n_id,"type":"thm","description":"This is a unique nodeeeeeee","importance":1})
				self.add_n(node)
				break
		return n_id

	def validate_input_nodes(self, nbunch):
		# checks that all given inputs exist in the graph
		if not self.acceptable_iterable(nbunch):
			nbunch = [nbunch]
		for node in nbunch:
			if not self.has_node(node):
				raise nx.NetworkXError('The input node {} is not in the graph'.format(node))
		return True

for key, value in _GraphExtended.__dict__.items():
	try:
		setattr(nx.Graph, key, value)
	except TypeError:
		pass
