############################# IMPORTS ############################
import sys
from warnings import warn
import subprocess
import copy
import re
import json
from string import punctuation

from lib import helper
from lib.vote import Votable

######################## INTERNAL HELPERS ########################
def to_bash():
	# include commands here to be executed in bash
	bash_out = subprocess.check_output('ls; cd; ls', shell=True)
	print(bash_out)
	subprocess.call('mkdir test_folder', shell=True)

def move_attribute(dic, aliases, strict=True):
	for key, value in dic.items():
		if key in aliases:
			del dic[key]
			return value
	if strict:
		raise KeyError('Could not find any of the following keys: {} in the soon-to-be Node {}.'.format(aliases, dic))
	else:
		return None

def is_capitalized(value):
	if re.search(r'[\$A-Z]', value): # starts with LaTeX or capital letter
		return True
	return False

def is_content_clean(value):
	if type(value) is list:
		for el in value:
			assert is_content_clean(el)
	if type(value) is str:
		assert len(value) >= 15 # arbitary length to make sure person actually put some content in
		assert is_capitalized(value) # we need to move this ONLY to the things that need to be capitalized (for example, not names)
		return True
	return True

def check_type_and_clean(value, value_type, list_of=False):
	if list_of:
		if type(value) is list:
			clean_value = []
			for el in value:
				if type(el) is value_type:
					if value_type is not str or el.strip() != '': # if value_type is str, we still exclude ''
						clean_value.append(el)
				elif (el is None or el.strip() == '') and value_type != 'NoneType' and value_type is not None:
					pass # ignore the blank entry
				else:
					raise Exception('Element {} is not of type {}'.format(el, value_type))
			value = clean_value
		elif value is None:
			value = []
		else:
			assert type(value) is value_type
			value = [value]
	else:
		assert type(value) is value_type
	return value

def find_key(dic, keys):
	for key in dic:
		if key in keys:
			return key
	raise KeyError('Could not find any of the following keys in the Node input: ' + str(keys))

def dunderscore_count(string):
	dunderscore_list = re.findall(r'__', string)
	return len(dunderscore_list)

def get_contents_of_dunderscores(string):
	list_contents = re.findall(r'(?<=__)[^_]*(?=__)', string) # we only want the first one, but contents is a list
	assert list_contents != [] and list_contents[0] != ""
	return list_contents[0]

def reduce_string(string):
	return re.sub(r'[_\W]', '', string).lower()

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
		raise ValueError('Cannot detect type of node.  "type" key has value: ' + dic['type'])

def find_node_from_id(list_of_nodes, ID):
	for node in list_of_nodes:
		if node.id == ID:
			return node
	warn('Could node find node with ID "' + ID + '" within list_of_nodes.')


############################## MAIN ##############################


class Node (Votable):


	MIN_IMPORTANCE = 1
	MAX_IMPORTANCE = 10
	# ALLOWED_ATTRIBUTES = ['name', 'id', 'type', 'importance', '_importance', 'description', 'intuitions', 'dependencies', 'examples', 'counterexamples', 'notes']

	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		empty_keys = []
		for key, value in dic.items():
			if value == "":
				empty_keys.append(key)
		for key in empty_keys:
			del dic[key]

		self.description = move_attribute(dic, {'description', 'content'}, strict=False)
		self.dependencies = move_attribute(dic, {'dependencies'}, strict=False)
		self.importance = move_attribute(dic, {'importance', 'weight'}, strict=False)
		self.intuitions = move_attribute(dic, {'intuitions', 'intuition'}, strict=False)
		self.examples = move_attribute(dic, {'examples', 'example'}, strict=False)
		self.counterexamples = move_attribute(dic, {'counterexample', 'counterexamples', 'counter example', 'counter examples'}, strict=False)
		self.notes = move_attribute(dic, {'note', 'notes'}, strict=False)
		self.name = move_attribute(dic, {'name'}, strict=False)

	@property
	def weight(self): # delete this if we get above to work
		pass
	@weight.setter
	def weight(self, new_weight):
		raise Exception('We are not using "weight" anymore.  We are using "importance".')

	def as_json(self): # returns json version of self
		return json.dumps(self.__dict__)

	def __str__(self):
		return str(self.__dict__)

	def __repr__(self):
		return 'Node(' + self.__str__() + ')'

	def __hash__(self):
		return hash(self.__dict__.values())

	def __eq__(self, other):
		return self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)

	def clone(self):
		return copy.deepcopy(self)

	@property
	def name(self):
		if '_name' in self.__dict__:
			return self._name
		else:
			return None
	@name.setter
	def name(self, new_name):
		if new_name is not None:
			assert dunderscore_count(new_name) == 0
			self._name = check_type_and_clean(new_name, str)
			self.id = self.name
		else:
			self._name = check_type_and_clean(new_name, type(None))

	@property
	def id(self):
		return self._id
	@id.setter
	def id(self, new_id_before_reduction):
		self._id = reduce_string(new_id_before_reduction)

	@property
	def type(self):
		return self._type
	@type.setter
	def type(self, new_type):
		clean_type = check_type_and_clean(new_type, str)
		if clean_type in {'definition', 'defn', 'def'}:
			self._type = 'definition'
		elif clean_type in {'axiom'}:
			self._type = 'axiom'
		elif clean_type in {'theorem', 'thm'}:
			self._type = 'theorem'
		elif clean_type in {'exercise'}:
			self._type = 'exercise'
		else:
			raise ValueError("Node's 'type' attribute must be a 'definition' (or 'defn' or 'def'), a 'theorem' (or 'thm'), or an 'exercise'.\nYOUR TYPE WAS: " + clean_type)

	@property
	def importance(self):
		return self._importance
	@importance.setter
	def importance(self, new_importance):
		if new_importance is not None:
			new_importance = check_type_and_clean(new_importance, int) # but in the future we will accept decimals (floats) too!
			assert new_importance >= self.MIN_IMPORTANCE and new_importance <= self.MAX_IMPORTANCE
		self._importance = new_importance

	@property
	def description(self):
		return self._description
	@description.setter
	def description(self, new_description):
		clean_description = check_type_and_clean(new_description, str)
		assert is_content_clean(clean_description)
		self._description = clean_description

	@property
	def intuitions(self):
		return self._intuitions
	@intuitions.setter
	def intuitions(self, new_intuitions):
		clean_intuitions = check_type_and_clean(new_intuitions, str, list_of=True)
		assert is_content_clean(clean_intuitions)
		for x in clean_intuitions:
			assert dunderscore_count(x) == 0
		self._intuitions = clean_intuitions

	@property
	def dependencies(self):
		return self._dependencies
	@dependencies.setter
	def dependencies(self, new_dependencies):
		cleaned_dependencies = check_type_and_clean(new_dependencies, str, list_of=True)
		for d in cleaned_dependencies:
			assert dunderscore_count(d) == 0
		self._dependencies = cleaned_dependencies

	@property
	def dependency_ids(self):
		return [reduce_string(x) for x in self.dependencies]

	@property
	def examples(self):
		return self._examples
	@examples.setter
	def examples(self, new_examples):
		cleaned_examples = check_type_and_clean(new_examples, str, list_of=True)
		assert is_content_clean(cleaned_examples)
		for x in cleaned_examples:
			assert dunderscore_count(x) == 0
		self._examples = cleaned_examples

	@property
	def counterexamples(self):
		return self._counterexamples
	@counterexamples.setter
	def counterexamples(self, new_counterexamples):
		cleaned_counterexamples = check_type_and_clean(new_counterexamples, str, list_of=True)
		assert is_content_clean(cleaned_counterexamples)
		for x in cleaned_counterexamples:
			assert dunderscore_count(x) == 0
		self._counterexamples = cleaned_counterexamples

	@property
	def notes(self):
		return self._notes
	@notes.setter
	def notes(self, new_notes):
		cleaned_notes = check_type_and_clean(new_notes, str, list_of=True)
		assert is_content_clean(cleaned_notes)
		# notes may mention a synonym, so we will allow dunderscores (open to discussion)
		self._notes = cleaned_notes


class Definition(Node):


	# ALLOWED_ATTRIBUTES = ['name', 'id', 'type', 'importance', 'description', 'intuitions', 'dependencies', 'examples', 'counterexamples', 'notes', 'plurals']

	def __init__(self,dic):
		super().__init__(dic)
		self.type = "definition"
		self.plurals = move_attribute(dic, {'plurals', 'plural', 'pl'}, strict=False)
		self.negation = move_attribute(dic, {'negation'}, strict=False)
		if self.importance is None:
			self.importance = 4
		if self.description is not None:
			assert dunderscore_count(self.description) >=2
		if self.name is None:
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
			# assert dunderscore_count(clean_negation) >= 2 # let's make BLINDS do that stuff INSTEAD
			self._negation = clean_negation

	@Node.description.setter
	def description(self, new_description):
		assert dunderscore_count(new_description) >= 2
		Node.description.fset(self, new_description)


class Axiom(Definition):


	def __init__(self, dic):
		super().__init__(dic)
		self.type = "axiom"

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
				Node.dependencies.fset(self, new_deps)
			else:
				raise KeyError('Axioms cannot have dependencies!')

	@Node.description.setter
	def description(self, new_description):
		if new_description is None:
			self._description = None
		else:
			assert dunderscore_count(new_description) >= 2
			Node.description.fset(self, new_description)


class PreTheorem(Node):


	# ALLOWED_ATTRIBUTES = ['name', 'id', 'type', 'importance', 'description', 'intuitions', 'dependencies', 'examples', 'counterexamples', 'notes', 'proofs']

	def __init__(self, dic):
		super().__init__(dic)
		self.proofs = move_attribute(dic, {'proofs', 'proof'}, strict=False)
		# theorems and exercises CANNOT have plurals: (but since we only created plural for Definitions, we shouldn't need this as long as there is a way to block undefined properties (see other Stack Overflow question))
		if 'plurals' in self.__dict__:
			raise KeyError('Theorems cannot have plurals.')

	@property
	def proofs(self):
		return self._proofs
	@proofs.setter
	def proofs(self, new_proofs):
		good_type_proofs = check_type_and_clean(new_proofs, dict, list_of=True)
		assert is_content_clean(good_type_proofs)
		for proof in good_type_proofs:
			proof['description'] = move_attribute(proof, {'description', 'content'}, strict=True)
			assert dunderscore_count(proof['description']) == 0
			assert 'type' in proof
			proof['type'] = check_type_and_clean(proof['type'], str, list_of=True)
		self._proofs = good_type_proofs

	@Node.description.setter
	def description(self, new_description):
		assert dunderscore_count(new_description) == 0
		Node.description.fset(self, new_description)


class Theorem(PreTheorem):


	MIN_IMPORTANCE = 3
	# ALLOWED_ATTRIBUTES = ['name', 'id', 'type', 'importance', 'description', 'intuitions', 'dependencies', 'examples', 'counterexamples', 'notes', 'proofs']


	def __init__(self, dic):
		super().__init__(dic)
		self.type = "theorem"
		if self.importance is None:
			self.importance = 6
		assert self.name is not None

	@PreTheorem.name.setter
	def name(self, new_name):
		assert new_name is not None
		PreTheorem.name.fset(self, new_name)


class Exercise(PreTheorem):


	MAX_IMPORTANCE = 3
	# ALLOWED_ATTRIBUTES = ['name', 'id', 'type', 'importance', 'description', 'intuitions', 'dependencies', 'examples', 'counterexamples', 'notes', 'proofs']

	def __init__(self, dic):
		super().__init__(dic)
		self.type = "exercise"
		if self.importance is None:
			self.importance = 1

	@PreTheorem.description.setter
	def description(self, new_description):
		PreTheorem.description.fset(self, new_description)
		if self.name is None:
			self.id = self.description
