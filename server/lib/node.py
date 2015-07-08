##################################### TODO ####################################
#Reg expressions for processing definition, name, etc..
#Stricter Reg Expressions with failure at else

# MathJax/Node.js, run bash commands from python script, export json
# update __repr__ and __str__ to follow Python standard
# To Do: Equality method, magic methods, people o-auth, login info

################################### IMPORTS ###################################
# standard library:
import sys
from warnings import warn
import subprocess
import copy
import re
import json

# local:
import helper

################################### HELPERS ###################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

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
		raise KeyError('Could not find any of the following keys in the Node input: ' + str(aliases))
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
		assert len(value) >= 1 # arbitary length to make sure person actually put some content in
		#assert value[-1] is '.' # make sure they end in period.  in future, support colon followed by a list without period?
		#assert is_capitalized(value)
		return True
	return True

def check_type_and_clean(value, value_type=str, list_of=False):
	if list_of:
		if type(value) is list:
			for el in value:
				assert type(el) is value_type
		elif value is None:
			value = []
		else:
			assert (type(value) is value_type or type(value) is dict)
			value = [value]
	else:
		assert (type(value) is value_type or type(value) is dict)
	return value

def find_key(dic, keys):
	for key in dic:
		if key in keys:
			return key
	raise KeyError('Could not find any of the following keys in the Node input: ' + keys)

def has_at_least_two_dunderscores(string):
	dunderscore_list = re.findall(r'__', string)
	return len(dunderscore_list) >= 2

#################################### MAIN #####################################


class Node:


	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		self.name = move_attribute(dic, {'name'})
		self.weight = move_attribute(dic, {'weight'})
		self.type = move_attribute(dic, {'type'}, strict=False)
		if self.type is None:
			self.type = find_key(dic, {'definition', 'defn', 'def', 'theorem', 'thm', 'exercise'})
		self.description = move_attribute(
			dic,
			{'description', 'content', 'definition', 'def', 'defn', 'theorem', 'thm', 'exercise'}
		)
		self.intuitions = move_attribute(dic, {'intuitions', 'intuition'}, strict=False)
		self.examples = move_attribute(dic, {'examples', 'example'}, strict=False)
		if self.type is 'theorem': # but this should be moved to Theorem class
			self.proofs = move_attribute(dic, {'proofs', 'proof'}, strict=False)
		if self.type is 'definition': # but this should be moved to Definition class?
			self.plural = move_attribute(dic, {'plural', 'pl'}, strict=False)
		for key in dic: # if one or more keys are still left in the dictionary...
			raise KeyError('Unexpected or redundant key "' + key + '" found in input dictionary.')


	def as_json(self): # returns json version of self
		return self.__dict__

	def __str__(self):
		if self.type=="definition":
			msg = "(%s,%s,%s,%s,%d)\n" % (self.name, self.plural, self.type, self.description, self.weight)
			if self._intuitions:
				for intuition in self._intuitions:
					msg = msg + self._intuitions + "\n"
			for example in self._examples:
				msg = msg + example + "\n"
			#for single_note in self._notes:
			#	msg=msg+ single_note+"\n"
		else:
			msg = "(%s,%s,%s,%d)\n" % (self.name,self.type,self.description,self.weight)
			if self._intuitions:
				for intuition in self._intuitions:
					msg = msg + intuition + "\n"
			for example in self._examples:
				msg = msg + example + "\n"
			#for single_note in self._notes:
			#	msg=msg+ single_note+"\n"
			for single_proof in self._proofs:
				for x in single_proof:
					msg=msg+str(x)+": "+single_proof[x]+"\n"
		return msg

	def __eq__(self,other):
		if self.name!=other.name:
			return False
		elif self.type!=other.type:
			return False
		elif self.weight!=other.weight:
			return False
		elif self.description!=other.description:
			return False
		for x in self.intuitions:
			if x not in other.intuitions:
				return False
		for x in self.examples:
			if x not in other.examples:
				return False
		#Matt Removed notes on last edit..
                #for x in self.notes:
		#	if x not in other.notes:
		#		return False
		return True

	def clone(self):
		return copy.deepcopy(self)

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, new_name):
		assert is_capitalized(new_name)
		self._name = check_type_and_clean(new_name, str)

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
	def weight(self):
		return self._weight
	@weight.setter
	def weight(self, new_weight):
		clean_weight = check_type_and_clean(new_weight, int) # but in the future we will accept decimals (floats) too!
		assert clean_weight >= 1 and clean_weight <= 10
		self._weight = clean_weight

	@property
	def description(self):
		return self._description
	@description.setter
	def description(self, new_description):
		clean_description = check_type_and_clean(new_description, str)
		# assert has_at_least_two_dunderscores(clean_description) # need this assertion for definitions!!!!
		assert is_content_clean(clean_description)
		self._description = clean_description

	@property
	def intuitions(self):
		return self._intuitions
	@intuitions.setter
	def intuitions(self, new_intuition):
		assert is_content_clean(new_intuition)
		self._intuitions = check_type_and_clean(new_intuition, str, list_of=True)
	def append_intuition(self, add_intuition):
		self._intuition.append(add_intuition)

	@property
	def examples(self):
		return self._examples
	@examples.setter
	def examples(self, new_examples):
		assert is_content_clean(new_examples)
		self._examples = check_type_and_clean(new_examples, str, list_of=True)
	def append_example(self, add_example):
		self._examples.append(add_example)

	@property
	def counterexamples(self):
		return self._examples
	@counterexamples.setter
	def counterexamples(self, new_examples):
		assert is_content_clean(new_examples)
		self._counterexamples = check_type_and_clean(new_examples, str, list_of=True)

	@property
	def notes(self):
		return self._notes
	@notes.setter
	def notes(self, new_notes):
		assert is_content_clean(new_notes)
		self._notes = check_type_and_clean(new_notes, str, list_of=True)
	def append_note(self, add_note):
		self._notes.append(add_note)

	@property
	def plural(self):
		return self._plural
	@plural.setter
	def plural(self, new_plural):
		if new_plural is None:
			return
		clean_plural = check_type_and_clean(new_plural, str)
		assert has_at_least_two_dunderscores(clean_plural)
		self._plural = clean_plural

	@property
	def proofs(self):
		return self._proofs
	@proofs.setter
	def proofs(self,new_proofs):
		assert is_content_clean(new_proofs)
		self._proofs = check_type_and_clean(new_proofs, str, list_of=True)
	def append_proof(self, add_proof): # these need type checking too
		self._proofs.append(add_proof)
