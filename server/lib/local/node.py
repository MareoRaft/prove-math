#!/usr/bin/env python3
################################### IMPORTS ###################################
# standard library:
#Reg expressions for processing definition, name, etc..
#Stricter Reg Expressions with failure at else
import sys
from warnings import warn
import subprocess
import copy
import re

# local:
import helper
from mongo import Mongo

################################### HELPERS ###################################
# Should we make mongo variables global for all methods?
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

def to_bash():
	# include commands here to be executed in bash
	bash_out = subprocess.check_output('ls; cd; ls', shell=True)
	print(bash_out)
	subprocess.call('mkdir test_folder', shell=True)


#################################### MAIN #####################################
# MathJax/Node.js, run bash commands from python script, export json
# update __repr__ and __str__ to follow Python standard
# To Do: Equality method, magic methods, people o-auth, login info


class Node:


	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):
		self.intuition = []
		self.examples = []
		self.notes = []
		self.proofs = []
		self.plural = None

		for key in dic.keys():
			if re.match(r'name$', key, re.IGNORECASE):
				self.name = dic[key]

			# re.match starts at the beginning of the string by default.
			# so re.match('hi$') is equivalent to re.search('^hi$')
			elif re.match(r'weight$', key, re.IGNORECASE):
				self.weight = dic[key]

			elif re.match(r'(?:theorem|thm)$', key, re.IGNORECASE):
				self.type = "theorem"
				self.description = dic[key]
				for ii in dic.keys(): # this needs to be restructured as we write things as subclasses
					if re.match(r'proofs?$', ii, re.IGNORECASE):
						if isinstance(dic[ii], dict):
							self.proofs.append(dic[ii])
						else:
							for x in dic[ii]:
								if isinstance(x,dict):
									self.proofs.append(x)

			elif re.match(r'(?:def|defn|definition)$', key, re.IGNORECASE):
				self.type = "definition"
				self.description = dic[key]
				if re.findall(r'__[^_]*__',dic[key]): # if no dunderscores are found, we should fail with an error message
					word=re.findall(r'__[^_]*__',dic[key])
					if len(word)==1:
						self.name=word[0].strip("__")
					else:
						compound_name=""
						for x in word:
							compound_name=compound_name+x.strip("__")+"/"
						self.name=compound_name.strip("/")

				for ii in dic.keys():
					if re.match(r'pl',ii,re.IGNORECASE):
						self.plural=dic[ii]

			elif re.match(r'type.*',key,re.IGNORECASE) and re.match(r'def.*',dic[key],re.IGNORECASE):
				self.type=dic[key]
				for ii in dic.keys():
					if re.match(r'pl',ii,re.IGNORECASE):
						self.plural=dic[ii]

			elif re.match(r'type.*',key,re.IGNORECASE) and re.match(r'th.*',dic[key],re.IGNORECASE):
				self.type=dic[key]
				for ii in dic.keys():
					if re.match(r'proof.*',ii,re.IGNORECASE):
						if isinstance(dic[ii],dict):
							self.proofs.append(dic[ii])
						else:
							for x in dic[ii]:
								self.proofs.append(x)


			elif re.match(r'des.*|contentmmmm',key,re.IGNORECASE) or re.match(r'content.*',key, re.IGNORECASE): # this needs to accept "content" as a synonym for description
				self.description=dic[key]

			elif re.match(r'intuit.*',key,re.IGNORECASE): # a lot of these seem like the same code, but one with "intuition", one with "example", one with "note", etc.  Try writing a function which takes in "intuition", etc, and does this so that you don't have to repeat the code.
				if isinstance(dic[key],list):
					for single_intuition in dic[key]:
						if isinstance(single_intuition,str):
							self.intuition.append(single_intuition)
				else:
					self.intuition = dic[key]

			elif re.match(r'example.*',key,re.IGNORECASE):
				if isinstance(dic[key],list):
					for single_examples in dic[key]:
						if isinstance(single_examples,str):
							self.examples.append(single_examples)
				else:
					self.examples.append(dic[key])

			elif re.match(r'note.*',key,re.IGNORECASE):
				if isinstance(dic[key],list):
					for single_notes in dic[key]:
						if isinstance(single_notes,str):
							self.notes.append(single_notes)
				else:
					self.notes.append(dic[key])

			else: output an error. key is not a valid key name.





	def __repr__(self):
		if self.type=="definition":
			msg = "(%s,%s,%s,%s,%d)\n" % (self.name, self.plural, self.type, self.description, self.weight)
			if self._intuition:
				msg = msg + self._intuition + "\n"
			for example in self._examples:
				msg = msg + example + "\n"
			for single_note in self._notes:
				msg=msg+ single_note+"\n"

		else:
			msg = "(%s,%s,%s,%d)\n" % (self.name,self.type,self.description,self.weight)
			if self._intuition:
				msg = msg + self._intuition + "\n"
			for example in self._examples:
				msg = msg + example + "\n"
			for single_note in self._notes:
				msg=msg+ single_note+"\n"
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
		for x in self.intuition:
			if x not in other.intuition:
				return False
		for x in self.examples:
			if x not in other.examples:
				return False
		for x in self.notes:
			if x not in other.notes:
				return False
		return True



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
		elif re.match(r'th.*', new_type):
			self._type = 'theorem'
		else:
			warn('Bad type. Must either be a theorem or definition')

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

	@description.setter
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
	@property
	def plural(self):
		return self._plural
	@plural.setter
	def plural(self, new_plural):
		self._plural=new_plural

	@property
	def proofs(self):
		return self._proofs

	@proofs.setter
	def proofs(self,new_proofs):
		self._proofs=new_proofs

	def append_proof(self, add_proof):
		self._proofs.append(add_proof)

	def append_intuition(self, add_intuition):
		self._intuition.append(add_intuition)

	def append_example(self, add_example):
		self._examples.append(add_example)

	def append_note(self, add_note):
		self._notes.append(add_note)

	def clone(self):
		clone = copy.deepcopy(self)
		return clone




# we should implement this stuff below and then delete the string:
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
