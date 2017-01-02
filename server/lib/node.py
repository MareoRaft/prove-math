############################# IMPORTS ############################
import sys
from warnings import warn
import subprocess
import re
import json
from copy import deepcopy

from lib import helper
from lib.helper import reduce_string, remove_outer_dunderscores, dunderscore_count
from lib.vote import Votable
from lib.config import ERR
from lib.score import ScoreCard
from lib.attr import Attr
from lib.node_config import ATTR_DICT

######################## INTERNAL HELPERS ########################
def move_attribute(dic, aliases, strict=True):
	for key, value in dic.items():
		if key in aliases:
			del dic[key]
			return value
	if strict:
		raise KeyError('Could not find any of the following keys: {} in the soon-to-be Node {}.'.format(aliases, dic))
	else:
		return None

def find_key(dic, keys):
	for key in dic:
		if key in keys:
			return key
	raise KeyError('Could not find any of the following keys in the Node input: {}'.format(keys))

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


	MIN_IMPORTANCE = 1
	MAX_IMPORTANCE = 10

	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		# populate type
		settings = ATTR_DICT['type']
		attr = Attr(name='type', **settings)
		setattr(self, attr.name, attr.value)

		# populate other attributes
		for name, settings in ATTR_DICT:
			value = move_attribute(dic, settings['keywords'], strict=False)
			del settings['keywords']
			attr = Attr(name=name, **settings)
			setattr(self, attr.name, attr.value)

		# populate id
		# similar to type

	def score_card(self):
		score_card = ScoreCard()
		for attr in self.attrs:
			score_card.extend(attr.score_card)
		return score_card

	def as_dict(self):
		dic = deepcopy(self.__dict__)
		if 'score_card' in dic:
			del dic['score_card']
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

	# a getter
	@property
	def dependency_ids(self):
		return [reduce_string(x) for x in self.dependencies]





class Definition(Node):


	def __init__(self,dic):
		super().__init__(dic)
		self.plurals = move_attribute(dic, {'plurals', 'plural', 'pl'}, strict=False)
		self.negation = move_attribute(dic, {'negation'}, strict=False)
		if self.importance is None:
			self.importance = 4
		if self.description in [None, '']:
			if self.name in [None, '']:
				self.score_card.strike("critical", ERR["NO_NAME"])
		else:
			if self.name in [None, ''] and dunderscore_count(self.description) < 2:
				self.score_card.strike("critical", ERR["NO_NAME"])
			if self.name not in [None, ''] and dunderscore_count(self.description) < 2:
				pass
			if self.name in [None, ''] and dunderscore_count(self.description) >= 2:
				self.name = get_contents_of_dunderscores(self.description)

	@property
	def plurals(self):
		return self._plurals
	@plurals.setter
	def plurals(self, new_plurals):
		if new_plurals is None:
			self._plurals = []
		else:
			cleaned_plurals = check_type_and_clean(new_plurals, str, list_of=True)
			self._plurals = cleaned_plurals

	@property
	def negation(self):
		return self._negation
	@negation.setter
	def negation(self, new_negation):
		if new_negation is None:
			self._negation = None
		else:
			clean_negation = check_type_and_clean(new_negation, str)
			clean_negation = remove_outer_dunderscores(clean_negation)
			if dunderscore_count(clean_negation) > 0:
				self.score_card.strike("medium", ERR["DUNDERSCORES"](clean_negation))
			self._negation = clean_negation

	@Node.description.setter
	def description(self, new_description):
		if new_description is None:
			new_description = ""
		if dunderscore_count(new_description) < 2:
			self.score_card.strike("low", ERR["NO_DUNDERSCORES"](new_description))
		Node.description.fset(self, new_description)


class Axiom(Definition):


	def __init__(self, dic):
		self.type = "axiom"
		super().__init__(dic)

	@property
	def dependencies(self):
		return []
	@dependencies.setter
	def dependencies(self, new_deps):
		if new_deps is None or (isinstance(new_deps, list) and not new_deps):
			self._dependencies = []
		else:
			if "justification" in dic:
				# as Mo pointed out, axioms CAN have dependencies.  Perhaps there are some definitions you create first, and then an AXIOM uses those definitions (but still introduces something you must accept on faith alone).
				pass
			else:
				# now we will even allow the user to make axioms with deps, so the fset is below this block.
				self.score_card.strike("medium", ERR["AXIOM_WITH_DEPENDENCY"])
		Node.dependencies.fset(self, new_deps)


class PreTheorem(Node):


	def __init__(self, dic):
		super().__init__(dic)
		print('BELOW COMMENTED OUT TO DISABLE PROOFS')
		# self.proofs = move_attribute(dic, {'proofs', 'proof'}, strict=False)



		# theorems and exercises CANNOT have plurals: (but since we only created plural for Definitions, we shouldn't need this as long as there is a way to block undefined properties (see other Stack Overflow question))
		if 'plurals' in self.as_dict():
			raise KeyError('Theorems cannot have plurals.')

	@property
	def proofs(self):
		return self._proofs
	@proofs.setter
	def proofs(self, new_proofs):
		good_type_proofs = check_type_and_clean(new_proofs, dict, list_of=True)
		self.validate_content_clean(good_type_proofs)
		for proof in good_type_proofs:
			proof['description'] = move_attribute(proof, {'description', 'content'}, strict=True)
			if dunderscore_count(proof['description']) > 0:
				self.score_card.strike("low", ERR["DUNDERSCORES"](proof['description']))
			if 'type' not in proof:
				self.score_card.strike("low", ERR["NO_PROOF_TYPE"])
				# then give some default type to the proof
				proof['type'] = None
			proof['type'] = check_type_and_clean(proof['type'], str, list_of=True)
		self._proofs = good_type_proofs

	@Node.description.setter
	def description(self, new_description):
		if dunderscore_count(new_description) != 0:
			self.score_card.strike("medium-high", ERR["DUNDERSCORES"](new_description))
		Node.description.fset(self, new_description)


class Theorem(PreTheorem):


	MIN_IMPORTANCE = 3

	def __init__(self, dic):
		self.type = "theorem"
		super().__init__(dic)
		if self.importance is None:
			self.importance = 6
		if self.name is None:
			self.score_card.strike("critical", ERR["NO_NAME"]) # maybe lower this if we can auto-assign a name

	@PreTheorem.name.setter
	def name(self, new_name):
		if new_name is not None:
			self.score_card.strike("critical", ERR["NO_NAME"]) # maybe lower this if we can auto-assign a name
		PreTheorem.name.fset(self, new_name)


class Exercise(PreTheorem):


	MAX_IMPORTANCE = 3

	def __init__(self, dic):
		self.type = "exercise"
		super().__init__(dic)
		if self.importance is None:
			self.importance = 1

	@PreTheorem.description.setter
	def description(self, new_description):
		PreTheorem.description.fset(self, new_description)
		if self.name is None:
			self.id = self.description
