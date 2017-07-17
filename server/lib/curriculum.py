from copy import deepcopy

from lib.mongo import Mongo
from lib import helper
from lib.vote import Votable

############################ HELPERS ############################
def unique_string(other_strings):
	unique_string = "a"
	while unique_string in other_strings:
		unique_string = helper.random_string(10)
	return unique_string


############################## MAIN ##############################


class Curriculum (Votable):


	NODES = Mongo("provemath", "nodes")
	CURRICULUMS = Mongo("provemath", "curriculums")

	def __init__(self, graph, init_method='node_ids', node_ids=[], destination=None, selected_nodes=[], name=None):
		self.name = name
		self.graph = graph
		self.init_method = init_method

		if self.init_method == 'node_ids':
			self.node_ids = node_ids
		elif self.init_method == 'destination':
			self.destination = destination
			self.selected_nodes = selected_nodes
			self.init_node_ids()
		else:
			raise ValueError('bad method')

		self.set_id()

		# TODO: verify the curriculum doesn't already exist? Allow override?

	def init_node_ids(self):
		node_ids = self.graph.linearized_predestinations2(self.destination, self.selected_nodes)
		self.node_ids = node_ids
		# should a curriculum even store this?  What is the graph changes, and the curriculum becomes logically invalid? -- i think the curriculum SHOULD store this, but there should be some VERIFY method that catches when a curriculum becomes invalid, and alerts the professor

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, new_name):
		if new_name is not None:
			if not isinstance(new_name, str):
				raise TypeError('Name must be a string.')
		self._name = new_name

	@property
	def id(self):
		return self._id
	def set_id(self):
		# make a unique id for the curriculum
		curriculums = list(self.CURRICULUMS.find())
		curriculum_ids = [c["_id"] for c in curriculums]
		self._id = unique_string(curriculum_ids)

	@property
	def node_ids(self):
		return self._node_ids
	@node_ids.setter
	def node_ids(self, node_ids):
		# verify nonempty
		if not node_ids:
			raise ValueError('A {} needs a NONEMPTY list of node ids.'.format(type(self).__name__))
		# verify that each node id actually exists
		for node_id in node_ids:
			next(self.NODES.find({"_id": node_id}))
			# the above should error if no node exists, so we have verified that the id exists
		# verify that node_ids follow LOGICAL order
		# or...at least..forward order.  this allows skipping over nodes
		assert self.graph.is_forward_order(node_ids)
		self._node_ids = node_ids

	def store(self):
		""" Store self in DB. """
		self.CURRICULUMS.insert_one(self.as_dict())

	def as_dict(self):
		d = deepcopy(self.__dict__)
		# we store the id under "_id", so nothing to adjust for mongo there
		del d['graph']
		del d['init_method']
		return d




