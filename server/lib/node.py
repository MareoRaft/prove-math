##################################### TODO ####################################
#Reg expressions for processing definition, name, etc..
#Stricter Reg Expressions with failure at else

# MathJax/Node.js, run bash commands from python script, export json
# people o-auth, login info

#7/14 Need to fix dunderscore issue

################################### IMPORTS ###################################
# standard library:
import sys
from warnings import warn
import subprocess
import copy
import re
import json
from string import punctuation

# local:
#Written as from lib import helper
from lib import helper

############################### INTERNAL HELPERS ###############################
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
		raise KeyError('Could not find any of the following keys: '+str(aliases)+' in the soon-to-be Node '+str(dic))
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
			for el in value:
				assert type(el) is value_type
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

############################### EXTERNAL HELPERS ###############################
def create_appropriate_node(dic):
	# for writers that use shortcut method, we must seek out the type:
	if not 'type' in dic:
		dic['type'] = find_key(dic, {'definition', 'defn', 'def', 'theorem', 'thm', 'exercise'})
		dic['description'] = move_attribute(dic, {'definition', 'defn', 'def', 'theorem', 'thm', 'exercise'})

	if dic['type'] in {'definition', 'defn', 'def'}:
		return Definition(dic)
	elif dic['type'] in {'theorem', 'thm'}:
		return Theorem(dic)
	elif dic['type'] == 'exercise':
		return Exercise(dic)
	else:
		raise ValueError('Cannot detect type of node.  "type" key has value: ' + dic['type'])

def find_node_from_id(nodes, ID):
	for node in nodes:
		if node._id == ID:
			return node
	raise Exception('Could node find node with ID: ' + ID + ' within the nodes: ' + nodes)


#################################### MAIN #####################################


class Node:


	MIN_IMPORTANCE = 1
	MAX_IMPORTANCE = 10

	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		empty_keys = []
		for key, value in dic.items():
			if value == "":
				empty_keys.append(key)
		for key in empty_keys:
			del dic[key]

		self.description = move_attribute(dic, {'description', 'content'}, strict=True)
		self.dependencies = move_attribute(dic, {'dependencies'}, strict=False)
		self.importance = move_attribute(dic, {'importance', 'weight'}, strict=False)
		self.intuitions = move_attribute(dic, {'intuitions', 'intuition'}, strict=False)
		self.examples = move_attribute(dic, {'examples', 'example'}, strict=False)
		self.counterexamples=move_attribute(dic, {'counterexample', 'counterexamples', 'counter example', 'counter examples'}, strict=False)
		self.notes = move_attribute(dic, {'note', 'notes'}, strict=False)
		self.name = move_attribute(dic, {'name'}, strict=False)

	def as_json(self): # returns json version of self
		return json.dumps(self.__dict__)

	def __str__(self):
		return str(self.__dict__)

	def __eq__(self,other):
		if self.name != other.name:
			return False
		elif self.type != other.type:
			return False
		elif self.importance != other.importance:
			return False
		elif self.description != other.description:
			return False
		for x in self.intuitions:
			if x not in other.intuitions:
				return False
		for x in self.examples:
			if x not in other.examples:
				return False
		for x in self.notes:
			if x not in other.notes:
				return False
		return True

	def clone(self):
		return copy.deepcopy(self)

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, new_name):
		if new_name is not None:
			assert dunderscore_count(new_name) == 0
			self._name = check_type_and_clean(new_name, str)
			self.id=self.name
		else:
			self._name= check_type_and_clean(new_name, type(None))
			
	@property
	def id(self):
		return self._id
	
	@id.setter
	def id(self,new_id):
		self._id=re.sub(r'[_\W]', ' ', new_id).lower().replace(" ","")

	@property
	def type(self):
		return self._type
	@type.setter
	def type(self, new_type):
		clean_type = check_type_and_clean(new_type, str)
		if clean_type in {'definition', 'defn', 'def'}:
			self._type = 'definition'
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
	def weight(self):
		pass
	@weight.setter
	def weight(self, new_weight):
		raise Exception('We are not using "weight" anymore.  We are using "importance".')

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
	def intuitions(self, new_intuition):
		assert is_content_clean(new_intuition)
		clean_intuitions = check_type_and_clean(new_intuition, str, list_of=True)
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
	def examples(self):
		return self._examples
	@examples.setter
	def examples(self, new_examples):
		assert is_content_clean(new_examples)
		cleaned_examples = check_type_and_clean(new_examples, str, list_of=True)
		for x in cleaned_examples:
			assert dunderscore_count(x) == 0
		self._examples = cleaned_examples

	@property
	def counterexamples(self):
		return self._counterexamples
	@counterexamples.setter
	def counterexamples(self, new_examples):
		assert is_content_clean(new_examples)
		cleaned_counterexamples = check_type_and_clean(new_examples, str, list_of=True)
		for x in cleaned_counterexamples:
			assert dunderscore_count(x) == 0
		self._counterexamples = cleaned_counterexamples

	@property
	def notes(self):
		return self._notes
	@notes.setter
	def notes(self, new_notes):
		assert is_content_clean(new_notes)
		cleaned_notes = check_type_and_clean(new_notes, str, list_of=True)
		# notes may mention a synonym, so we will allow dunderscores (open to discussion)
		self._notes = cleaned_notes


class Definition(Node):


	def __init__(self,dic):
		super().__init__(dic)
		self.type = "definition"
		self.plural = move_attribute(dic, {'plural', 'pl'}, strict=False)
		if self.importance is None:
			self.importance = 4
		assert dunderscore_count(self.description) >=2
		if self.name is None:
			self.name = get_contents_of_dunderscores(self.description)

	@property
	def plural(self):
		return self._plural
	@plural.setter
	def plural(self, new_plural):
		if new_plural is None:
			self._plural = None
		else:
			clean_plural = check_type_and_clean(new_plural, str)
			assert dunderscore_count(clean_plural) >= 2
			self._plural = clean_plural

	@Node.description.setter
	def description(self, new_description):
		assert dunderscore_count(new_description) >= 2
		Node.description.fset(self, new_description)


class PreTheorem(Node):


	def __init__(self, dic):
		super().__init__(dic)
		self.proofs = move_attribute(dic, {'proofs', 'proof'}, strict=False)
		# theorems and exercises CANNOT have plurals: (but since we only created plural for Definitions, we shouldn't need this as long as there is a way to block undefined properties (see other Stack Overflow question))
		if 'plural' in self.__dict__:
			raise KeyError('Theorems cannot have plurals.')

	@property
	def proofs(self):
		return self._proofs
	@proofs.setter
	def proofs(self, new_proofs):
		good_type_proofs = check_type_and_clean(new_proofs, dict, list_of=True)
		assert is_content_clean(good_type_proofs)
		for proof in good_type_proofs:
			print('proof is '+str(proof))
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

	def __init__(self, dic):
		super().__init__(dic)
		self.type = "theorem"
		if self.importance is None:
			self.importance = 6
		assert self.name is not None

	@PreTheorem.name.setter
	def name(self, new_name):
		assert new_name is not None
		assert is_capitalized(new_name)
		PreTheorem.name.fset(self, new_name)


class Exercise(PreTheorem):


	MAX_IMPORTANCE = 3

	def __init__(self, dic):
		super().__init__(dic)
		self.type = "exercise"
		if self.importance is None:
			self.importance = 1
	
	@PreTheorem.description.setter
	def description(self, new_description):
		self.id=new_description
		PreTheorem.description.fset(self,new_description)
