############################ IMPORTS #############################
import time
from warnings import warn

import networkx as nx

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

	def add_node_unique(self):
		while True:
			print('adding a UNIQUE node.  This could be a problem because "custom_object" doesn\'t exist!')
			n = 'node_unique.' + string_unique()
			if self.has_node(n):
				warn('The node already existed.')
				continue
			else:
				self.add_node(n)
				break
		return n

	def validate_input_nodes(self, nbunch):
		# checks that all given inputs exist in the graph
		if not self.acceptable_iterable(nbunch):
			nbunch = [nbunch]
		for node in nbunch:
			if not self.has_node(node):
				raise nx.NetworkXError('The input node {0} is not in the graph'.format(node))
		return True

for key, value in _GraphExtended.__dict__.items():
	try:
		setattr(nx.Graph, key, value)
	except TypeError:
		pass
