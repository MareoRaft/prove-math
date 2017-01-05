############################# IMPORTS ############################
import sys
from warnings import warn
import subprocess
import re
import json
from copy import deepcopy

from lib import helper
from lib.helper import reduce_string, dunderscore_count, move_attribute, find_key
from lib.vote import Votable
from lib.config import ERR
from lib.score import ScoreCard
from lib.attr import Attr
from lib.node_config import NODE_MIN_IMPORTANCE, NODE_MAX_IMPORTANCE, THEOREM_MIN_IMPORTANCE, EXERCISE_MAX_IMPORTANCE, NODE_ATTR_SETTINGS, DEFINITION_ATTR_SETTINGS, AXIOM_ATTR_SETTINGS, PRETHEOREM_ATTR_SETTINGS, THEOREM_ATTR_SETTINGS, EXERCISE_ATTR_SETTINGS

######################## INTERNAL HELPERS ########################
def get_contents_of_dunderscores(string):
	list_contents = re.findall(r'(?<=__)[^_]*(?=__)', string) # we only want the first one, but contents is a list
	assert list_contents != [] and list_contents[0] != ""
	return list_contents[0]

######################## EXTERNAL HELPERS ########################
def create_appropriate_node(dic):
	# for writers that use shortcut method, we must seek out the type:
	if not 'type' in dic:
		dic['type'] = find_key(dic, {'axiom', 'definition', 'defn', 'def', 'theorem', 'thm', 'exercise'})
		dic['description'] = move_attribute(dic, {'axiom', 'definition', 'defn', 'def', 'theorem', 'thm', 'exercise'})

	if dic['type'] in {'definition', 'defn', 'def'}:
		return Definition(dic)
	elif dic['type'] == 'axiom':
		return Axiom(dic)
	elif dic['type'] in {'theorem', 'thm'}:
		return Theorem(dic)
	elif dic['type'] == 'exercise':
		return Exercise(dic)
	else:
		raise ValueError('Cannot detect type of node.  "type" key has value: {}'.format(dic['type']))

def find_node_from_id(list_of_nodes, ID):
	for node in list_of_nodes:
		if node.id == ID:
			return node
	warn('Could node find node with ID "{}" within list_of_nodes.'.format(ID))


############################## MAIN ##############################


class Node(Votable):


	ATTR_SETTINGS = NODE_ATTR_SETTINGS

	MIN_IMPORTANCE = NODE_MIN_IMPORTANCE
	MAX_IMPORTANCE = NODE_MAX_IMPORTANCE

	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		# populate attributes, excluding type, id, and dependency ids
		self.attrs = dict()
		self.update_attrs_from_dict(dic, self.ATTR_SETTINGS)

	# getter attributes...
	@property
	def type(self):
		return type(self).__name__.lower()

	@property
	def id(self):
		if self.attrs['name'].value != '':
			return reduce_string(self.attrs['name'].value)
		elif self.type == 'exercise':
			return reduce_string(self.attrs['description'].value)

	@property
	def dependency_ids(self):
		return [reduce_string(x) for x in self.attrs['dependencies'].value]

	# other methods...
	def update_attrs_from_dict(self, dic, settings_dict):
		for name, settings in settings_dict.items():
			print('name {}'.format(name))
			print('settings {}'.format(settings))
			value = move_attribute(dic, settings['keywords'], strict=False)

			# edit the settings, without altering self.ATTR_SETTINGS itself
			settings_new = deepcopy(settings)
			del settings_new['keywords']

			attr = Attr(node=self, name=name, value=value, **settings_new)
			self.attrs[name] = attr

	def score_card(self):
		score_card = ScoreCard()
		for attr in self.attrs:
			score_card.extend(attr.score_card)
		return score_card

	def as_dict(self):
		dic = deepcopy(self.__dict__)
		dic.update({
			"id": self.id,
			"dependency_ids": self.dependency_ids,
		})
		dic['attrs'] = {key: val.as_dict() for key, val in dic['attrs'].items()}
		return dic

	def as_json(self): # returns json version of self
		return json.dumps(self.as_dict())

	def __str__(self):
		return str(self.as_dict())

	def __repr__(self):
		return 'Node({})'.format(self)

	def __hash__(self):
		return hash(self.as_dict().values())

	def __eq__(self, other):
		return self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)


class Definition(Node):


	ATTR_SETTINGS = DEFINITION_ATTR_SETTINGS

	def __init__(self, dic):
		super().__init__(dic)

		# penalize empty name
		if self.attrs['description'].value in [None, '']:
			if self.attrs['name'].value in [None, '']:
				self.attrs['name'].score_card.strike("critical", ERR["NO_NAME"])
		else:
			if self.attrs['name'].value in [None, ''] and dunderscore_count(self.attrs['description'].value) < 2:
				self.attrs['name'].score_card.strike("critical", ERR["NO_NAME"])
			if self.attrs['name'].value not in [None, ''] and dunderscore_count(self.attrs['description'].value) < 2:
				self.attrs['name'].score_card.strike("critical", ERR["NO_NAME"])
			if self.attrs['name'].value in [None, ''] and dunderscore_count(self.attrs['description'].value) >= 2:
				self.attrs['name'].value = get_contents_of_dunderscores(self.attrs['description'].value)


class Axiom(Definition):


	ATTR_SETTINGS = AXIOM_ATTR_SETTINGS


class PreTheorem(Node):


	ATTR_SETTINGS = PRETHEOREM_ATTR_SETTINGS


class Theorem(PreTheorem):


	ATTR_SETTINGS = THEOREM_ATTR_SETTINGS

	MIN_IMPORTANCE = THEOREM_MIN_IMPORTANCE


class Exercise(PreTheorem):


	ATTR_SETTINGS = EXERCISE_ATTR_SETTINGS

	MAX_IMPORTANCE = EXERCISE_MAX_IMPORTANCE

