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

	def __init__(self, node_ids, name=None):
		self.name = name
		self.ids = node_ids
		self.set_id()

		# TODO: verify the curriculum doesn't already exist? Allow override?

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, new_name):
		if new_name is not None:
			if not isinstance(new_name, str):
				raise ValueError('Name must be a string.')
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
	def ids(self):
		return self._ids
	@ids.setter
	def ids(self, node_ids):
		# verify nonempty
		if not node_ids:
			raise ValueError('A {} needs a NONEMPTY list of node ids.'.format(type(self).__name__))
		# verify that each node id actually exists
		for node_id in node_ids:
			next(self.NODES.find({"_id": node_id}))
			# the above should error if no node exists, so we have verified that the id exists
		# TODO: verify that node_ids follow LOGICAL order?
		self._ids = node_ids

	def store(self):
		""" Store self in DB. """
		self.CURRICULUMS.insert_one(self.as_dict())

	def as_dict(self):
		d = deepcopy(self.__dict__)
		# store the id under "_id", so nothing to adjust for mongo
		return d




