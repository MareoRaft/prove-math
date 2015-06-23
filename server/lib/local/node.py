#!/usr/bin/env python3
################################### IMPORTS ###################################
# standard library:
import sys
from warnings import warn
import subprocess
import copy
import re

# third party:
import pymongo

# local:
#It appears that helper has been moved to the parent directory
sys.path.insert(0, '..')
import helper

################################### HELPERS ###################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

def to_bash():
	# include commands here to be executed in bash
	bash_out = subprocess.check_output('ls; cd; ls', shell=True)
	print (bash_out)
	subprocess.call('mkdir test_folder', shell=True)

def insert_to_mongo(dic):
	connection = pymongo.MongoClient("mongodb://localhost")
	db = connection.test
	people = db.people

	matt = {"name": "Elliot", "company": "Picatinny", "interests": "engineering"}

	try:
		people.insert_one(dic)


	except Exception as e:
		print("Unexpected error:")


#################################### MAIN #####################################
# I would like to make a python3 script which uses this class and allows me to manually input new definitions, theorems, lemmas, etc.
# def vs definition, make clone a method, node is capitalized
# MathJax/Node.js, run bash commands from python script, export json
# update __repr__ and __str__ to follow Python standard
# To Do: Equality method, magic methods, people o-auth, login info


class Node:


	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		self.name = dic["name"] # Thanks to the @name.setter, we can (and should) use self.name = value syntax.
		self.type = dic["type"]
		self.weight = dic["weight"]
		self.description = dic["description"]
		self.intuition = []
		self.examples = []
		self.notes = []
		if "intuition" in dic:
			self.intuition = dic["intuition"]
		if "examples" in dic:
			for single_examples in dic["examples"]:
				self.examples.append(single_examples)

		if "notes" in dic:
			for single_notes in dic["notes"]:
				self.notes.append(single_notes)

	def __repr__(self):
		msg = "(%s,%s,%s,%d)\n" % (self._name,self._type,self._description,self._weight)
		if self._intuition:
			msg = msg + self._intuition + "\n"
		for example in self._examples:
			msg = msg + example + "\n"
		return msg

	@property
	def name(self):
		return self._name # Here, and...

	@name.setter
	def name(self, new_name):
		self._name = new_name # ...here are the only places where we access the private _name attribute.

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, new_type):
		if re.match(r'def.*', new_type):
			self._type = 'definition'
		elif re.match(r'theor.*', new_type):
			self._type = 'theorem'
		else:
			warn('Bad type.')

	@property
	def weight(self):
		return self._weight

	@weight.setter
	def weight(self, new_weight):
		if isinstance(new_weight, (int, float)):
			self._weight = new_weight
		else:
			warn('Weight must be a number.')

	@property
	def description(self):
		return self._description

	@weight.setter
	def description(self, new_description):
		self._description = new_description

	@property
	def intuition(self):
		return self._intuition

	@intuition.setter
	def intuition(self, new_intuition):
		self._intuition = new_intuition

	@property
	def examples(self):
		return self._examples

	@examples.setter
	def examples(self, new_examples):
		self._examples = new_examples

	@property
	def notes(self):
		return self._notes

	@notes.setter
	def notes(self, new_notes):
		self._notes = new_notes

	def append_intuition(self, add_intuition):
		self._intuition.append(add_intuition)

	def append_example(self, add_example):
		self._examples.append(add_example)

	def append_note(self, add_note):
		self._notes.append(add_note)

	def clone(self):
		clone = copy.deepcopy(self)
		return clone


if __name__=="__main__":

	print("Hello World")
	sample_theorem = {"name": "Pythagorean theorem", "type": "theorem", "weight": 1, "description": "a^2+b^2=c^2", "intuition": "A simple explanation", "examples": ["Example 1", "Example 2"]}
	sample_definition = {"name": "triangle", "type": "definition", "weight": 1, "description": "3 sided polygon", "intuition": "A simple explanation", "examples": ["Example 1", "Example 2"]}
	a = Node(sample_theorem)
	b = Node(sample_definition)
	print(a)
	print(b)
	#Importing the same documents from a file
	data_dictionary = helper.json_import('../../data/data-test.json')
	for x in data_dictionary['nodes']:
		c = Node(x)
		insert_to_mongo(c.__dict__)
		print(c)

	# Test the clone function
	test_clone = a.clone()
	test_clone.name = "LALATheorem"
	print(test_clone)
	print(a)


	# Test the export function
	to_file = [a.__dict__,b.__dict__]
	helper.json_export(to_file, 'test.txt')

	#Test the subprocess/bash function
	to_bash()

	#Test the pymongo insert
	insert_to_mongo(b.__dict__)








"""
	@definition.setter
	def definition(self, definition):
		if not definition has underlined word:
			warn('No underlined word.')
		else if not definition satisfies some definition specific thing:
			warn('Doesn\'t have thing')
		else:
			self.__definition = definition

	# other properties will follow the same model as above (but i won't bother until the above is tested and works nicely)

	def intuition(self, intuition):
		if intuition is not something bad about intuitions:
			warn('bad')
		else:
			self.__intuition = intuition


	# run all keys through lowercasation, and convert thm-->theorem, def-->definition, ex-->exercise, pf-->proof-->proofs, pl-->plural,
	# general things for ALL properties: 1. not shorter than 15 characters 2. ends in period 3. starts with LaTeX or capital letter

	# def examples # array of examples

	# def counter_examples
"""
