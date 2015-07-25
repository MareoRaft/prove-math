#7/14 Need to fix dunderscore issue
##################################### TODO ####################################
#Reg expressions for processing definition, name, etc..
#Stricter Reg Expressions with failure at else

# MathJax/Node.js, run bash commands from python script, export json
# people o-auth, login info

################################### IMPORTS ###################################
# standard library:
import sys
from warnings import warn
import subprocess
import copy
import re
import json

# local:
#Written as from lib import helper
from lib import helper

################################### HELPERS ###################################
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
	raise KeyError('Could not find any of the following keys in the Node input: ' + keys)

def dunderscore_count(string):
	dunderscore_list = re.findall(r'__', string)
	return len(dunderscore_list)




#################################### MAIN #####################################


class Node:


	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		#self.type = move_attribute(dic, {'type'}, strict=False)
		#if self.type is None:
		#	self.type = find_key(dic, {'definition', 'defn', 'def', 'theorem', 'thm', 'exercise'})
		self.description = move_attribute(
			dic,
			{'description', 'content'}
		)
		self.importance = move_attribute(dic, {'importance', 'weight'})
		self.intuitions = move_attribute(dic, {'intuitions', 'intuition'}, strict=False)
		self.examples = move_attribute(dic, {'examples', 'example'}, strict=False)
		self.counterexamples=move_attribute(dic,{'counterexample','counterexamples','counter_example','counter_examples'},strict=False)
		self.notes=move_attribute(dic,{'note','notes'},strict=False)
		if self.type is 'exercise':
			self.name = move_attribute(dic, {'name'},strict=False)
		else:
			self.name = move_attribute(dic, {'name'})



	def as_json(self): # returns json version of self
		return self.__dict__

	def __str__(self):
		msg=""
		if self.intuitions:
			for intuition in self.intuitions:
				msg = msg + intuition + "\n"
		if self.examples:
			for example in self.examples:
				msg = msg + example + "\n"
		if self.counterexamples:
			for counter in self.counterexamples:
				msg=msg+counter+"\n"
		if self.notes:
			for single_note in self.notes:
				msg=msg+ single_note+"\n"

		if self.type=="definition":
			first_part = "(%s,%s,%s,%s,%d)\n" % (self.name, self.plural, self.type, self.description, self.importance)

		else:
			first_part = "(%s,%s,%s,%d)\n" % (self.name,self.type,self.description,self.importance)
			if self.proofs:
				for single_proof in self.proofs:
					for x in single_proof:
						msg=msg+str(x)+": "+single_proof[x]+"\n"
		return first_part+msg

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
		if new_name:
			assert is_capitalized(new_name)
			assert dunderscore_count(new_name)==0;
			self._name = check_type_and_clean(new_name, str)
		else:
			self._name= check_type_and_clean(new_name, type(None))


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
		clean_importance = check_type_and_clean(new_importance, int) # but in the future we will accept decimals (floats) too!
		assert clean_importance >= 1 and clean_importance <= 10
		self._importance = clean_importance

	@property
	def description(self):
		return self._description
	@description.setter
	def description(self, new_description):
		clean_description = check_type_and_clean(new_description, str)
		if self.type=='definition':
			assert dunderscore_count(clean_description) >=2 # need this assertion for definitions!!!!
		else:
			assert dunderscore_count(clean_description)==0
		assert is_content_clean(clean_description)
		self._description = clean_description

	@property
	def intuitions(self):
		return self._intuitions
	@intuitions.setter
	def intuitions(self, new_intuition):
		assert is_content_clean(new_intuition)
		cleaned_intuition = check_type_and_clean(new_intuition, str, list_of=True)
		for x in cleaned_intuition:
			assert dunderscore_count(x)==0
		self._intuitions=cleaned_intuition

	def append_intuition(self, add_intuition):
		assert is_content_clean(add_intuition)
		assert dunderscore_count(add_intuition)==0
		self._intuition.append(add_intuition)

	@property
	def examples(self):
		return self._examples

	@examples.setter
	def examples(self, new_examples):
		assert is_content_clean(new_examples)
		cleaned_examples = check_type_and_clean(new_examples, str, list_of=True)
		for x in cleaned_examples:
			assert dunderscore_count(x)==0
		self._examples=cleaned_examples

	def append_example(self, add_example):
		assert is_content_clean(add_example)
		assert dunderscore_count(add_example)==0
		self._examples.append(add_example)

	@property
	def counterexamples(self):
		return self._counterexamples
	@counterexamples.setter
	def counterexamples(self, new_examples):
		assert is_content_clean(new_examples)
		cleaned_counterexamples = check_type_and_clean(new_examples, str, list_of=True)
		for x in cleaned_counterexamples:
			assert dunderscore_count(x)==0
		self._counterexamples=cleaned_counterexamples

	def append_counterexample(self, add_counterexample):
		assert is_content_clean(add_counterexample)
		assert dunderscore_count(add_counterexample)==0
		self._examples.append(add_counterexample)


	@property
	def notes(self):
		return self._notes
	@notes.setter
	def notes(self, new_notes):
		assert is_content_clean(new_notes)
		cleaned_notes = check_type_and_clean(new_notes, str, list_of=True)
		for x in cleaned_notes:
			assert dunderscore_count(x)==0
		self._notes=cleaned_notes

	def append_note(self, add_note):
		assert is_content_clean(add_note)
		assert dunderscore_count(add_note)==0
		self._notes.append(add_note)


class Definition(Node):


	def __init__(self,dic):
		self.type = "definition"
		super(Definition, self).__init__(dic)
		self.plural = move_attribute(dic, {'plural', 'pl'}, strict=False)


	@property
	def plural(self):
		return self._plural

	@plural.setter
	def plural(self, new_plural):
		if new_plural is None:
			self._plural = None
		else:
			clean_plural = check_type_and_clean(new_plural, str)
			assert dunderscore_count(clean_plural)>=2
			self._plural = clean_plural


class Theorem(Node):
	def __init__(self, dic):
		self.type = "theorem"
		super(Theorem, self,).__init__(dic)
		self.proofs = move_attribute(dic, {'proofs', 'proof'}, strict=False)


	#Override the importance setter for specific Theorem importance
	@property
	def importance(self):
		return self._importance

	@importance.setter
	def importance(self, new_importance):
		clean_importance = check_type_and_clean(new_importance, int) # but in the future we will accept decimals (floats) too!
		assert clean_importance >= 3 and clean_importance <= 10
		self._importance = clean_importance

	@property
	def proofs(self):
		return self._proofs

	@proofs.setter
	def proofs(self,new_proofs):
		assert is_content_clean(new_proofs)
		self._proofs = check_type_and_clean(new_proofs, dict, list_of=True)

	def append_proof(self, add_proof): # these need type checking too
		self._proofs.append(add_proof)


class Exercise(Node):
	def __init__(self, dic):
		self.type = "exercise"
		super(Exercise, self).__init__(dic)
		self.proofs = move_attribute(dic, {'proofs', 'proof'}, strict=False)

	@property
	def importance(self):
		return self._importance

	@importance.setter
	def importance(self, new_importance):
		clean_importance = check_type_and_clean(new_importance, int)
		assert clean_importance >= 1 and clean_importance <= 3
		self._importance = clean_importance


	@property
	def proofs(self):
	       	return self._proofs

	@proofs.setter
	def proofs(self,new_proofs):
	       	assert is_content_clean(new_proofs)
	       	self._proofs = check_type_and_clean(new_proofs, dict, list_of=True)
	def append_proof(self, add_proof): # these need type checking too
		self._proofs.append(add_proof)


