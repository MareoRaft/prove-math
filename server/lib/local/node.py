#!/usr/bin/env python3
################################### IMPORTS ###################################
# standard library:
#Reg expressions for processing definition, name, etc..
#Mongo class 
import sys
from warnings import warn
import subprocess
import copy
import re


# local:
#It appears that helper has been moved to the parent directory
sys.path.insert(0, '..')
import helper
import mongo


################################### HELPERS ###################################
# Should we make mongo variables global for all methods?
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

def to_bash():
	# include commands here to be executed in bash
	bash_out = subprocess.check_output('ls; cd; ls', shell=True)
	print (bash_out)
	subprocess.call('mkdir test_folder', shell=True)


#################################### MAIN #####################################
# I would like to make a python3 script which uses this class and allows me to manually input new definitions, theorems, lemmas, etc.
# def vs definition, make clone a method, node is capitalized
# MathJax/Node.js, run bash commands from python script, export json
# update __repr__ and __str__ to follow Python standard
# To Do: Equality method, magic methods, people o-auth, login info


class Node:


	# Pass in a single json dictionary (dic) in order to convert to a node
	def __init__(self, dic):

					
		self.intuition = []
		self.examples = []
		self.notes = []
		self.proofs=[]
		self.plural=None

		for key in dic.keys():
			if re.match(r'name.*',key, re.IGNORECASE):
				self.name = dic[key]
			
			elif re.match(r'weight.*',key,re.IGNORECASE):
				self.weight = dic[key]
			
			elif re.match(r'th.*',key,re.IGNORECASE):
				self.type="theorem"
				self.description=dic[key]
				for ii in dic.keys():
					if re.match(r'proof.*',ii,re.IGNORECASE):
						if isinstance(dic[ii],dict):
							self.proofs.append(dic[ii])
						else:
							for x in dic[ii]:
								if isinstance(x,dict):
									self.proofs.append(x)
			
			elif re.match(r'def.*',key,re.IGNORECASE):
				self.type="definition"
				self.description=dic[key]
				if re.findall(r'__[^_]*__',dic[key]):
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
			

			elif re.match(r'des.*',key,re.IGNORECASE) or re.match(r'content.*',key, re.IGNORECASE):
				self.description=dic[key]
			
			elif re.match(r'intuit.*',key,re.IGNORECASE):
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
			
			#At this point python will begin guessing
			elif  isinstance(dic[key], str) and  re.search(r'__[^_]*__',dic[key]):
				self.type="definition"
				self.description=dic[key]
				word=re.findall(r'__[^_]*__',dic[key]).group()
				if len(word)==1:
					self.name=word.strip("__")
				else:
					compound_name=""
					for x in word:
						compound_name=compound_name+x.strip("__")+"/"
					self.name=compound_name.strip("/")


			elif isinstance(dic[key], str) and re.search(r'\$',dic[key]):
				self.type="theorem"
				self.description=dic[key]

				

				


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


if __name__=="__main__":

	sample_theorem = {"name": "Pythagorean theorem", "type": "theorem", "weight": 1, "description": "a^2+b^2=c^2", "intuition": "A simple explanation", "examples": ["Example 1", "Example 2"]}
	sample_definition = {"name": "triangle","plural":"triangles", "type": "definition", "weight": 1, "description": "3 sided polygon", "intuition": "A simple explanation", "examples": ["Example 1", "Example 2"]}
	matt_example1=	{
			"name": "Choosy Identity",
			"weight": 3,
			"thm": "$ \\binom nk = \\binom{n}{n-k} $",
			"proofs": [
				"Apply $\\binom nk = \\frac{n!}{k!(n-k)!} = \\frac{n!}{[n-(n-k)]!(n-k)!} = \\binom{n}{n-k} $",
				{
					"type": "combinatorial",
					"content": "Left side: We have $n$ puppies.  We choose $k$ of them and color them blue.  We color the rest of them red.  Right side: We have $n$ puppies.  We choose $n-k$ of them and color them red.  We color the rest of them blue.",
				},
			],
		}

	matt_example2=	{
			"weight": 4,
			"type": "exercise",
			"content": "$ k \\binom nk = n \\binom{n-1}{k-1} $",
			"proof": {
				"type": "combinatorial",
				"content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee.",
			},
		}

	thomas_example=	{"definition":"If $E \subset S$, and $\exists \gamma \in S$ such that $\forall x \in E, x \geq \gamma$, then we say that $E$ is __bounded below__ by $\gamma"}

	thomas_example_1={"definition":"If $E$ is __bounded gamma__ by $\gamma$, then we say that $\gamma$ is a __lower bound__ of $E$"}



	#a = Node(sample_theorem)
	#b = Node(sample_definition)
	#c= Node(matt_example1)
	#d=Node(matt_example2)
	#e=Node(thomas_example)
	#f=Node(thomas_example_1)
	#print(a)
	#print(b)
	#print(c)
	#print(d.__dict__)
	#print(e.__dict__)
	#print(f.__dict__)
        #Importing the same documents from a file
	
	data_dictionary = helper.json_import('../../data/data-test.json')
	for x in data_dictionary['nodes']:
		c = Node(x)
		#print(c)

	new_data_dictionary = helper.json_import('../../data/commas-removed.json')
	for x in new_data_dictionary['nodes']:
		c=Node(x)
		#print(c.__dict__)




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
