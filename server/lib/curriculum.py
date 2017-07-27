from copy import deepcopy

from lib.mongo import Mongo
from lib import helper
from lib.vote import Votable

############################ HELPERS ############################
NODES = Mongo("provemath", "nodes")
CURRICULUMS = Mongo("provemath", "curriculums")

def unique_string(other_strings):
	unique_string = "a"
	while unique_string in other_strings:
		unique_string = helper.random_string(10)
	return unique_string

def get_all_curriculum_ids():
		curriculums = list(CURRICULUMS.find())
		curriculum_ids = [c["_id"] for c in curriculums]
		return curriculum_ids


############################## MAIN ##############################


class Curriculum(Votable):


	def __init__(self, node_ids, name=None, retrieve=False, wanted_id=None):
		"""
		If retrieve is True, it will look for the curriculum by id in the DB.  if it exists, create the object.  Otherwise, fail.
		"""
		if retrieve:
			# retrieve Curriculum from DB
			if id is None:
				raise ValueError('no curriculum_id to retrieve curriculum with')
			curriculum_ids = get_all_curriculum_ids()
			if wanted_id not in curriculum_ids:
				raise ValueError('That curriculum_id doesn\'t exist in the database!')
			curriculum_dict = CURRICULUMS.find_one({"_id": wanted_id})
			self.name = curriculum_dict['name']
			self._id = curriculum_dict['_id'] # bypass setter, since we already know it's right
			self.node_ids = curriculum_dict['node_ids']
		else:
			# create new Curriculum and store in DB
			self.name = name
			self.node_ids = node_ids
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
		curriculum_ids = get_all_curriculum_ids()
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
		# TODO: verify that node_ids follow LOGICAL order?
		self._node_ids = node_ids

	def store(self):
		""" Store self in DB. """
		CURRICULUMS.insert_one(self.as_dict())

	def as_dict(self):
		d = deepcopy(self.__dict__)
		# store the id under "_id", so nothing to adjust for mongo
		return d

	def as_printable_html(self):
		string = ''
		for node_id in self.node_ids:
			node = NODES.find_one({"_id": node_id})
			string = string + node.as_printable_html()
		return string


