# I would like to make a python3 script which uses this class and allows me to manually input new definitions, theorems, lemmas, etc.
#5/18 Theo was here
# Next-Clone, setters/getters, read from file


from warnings import warn
import json


class node:

	# Pass in a single json doc in order to convert to a node
	def __init__(self, doc):
		self.name=doc["name"]
		self.type=doc["type"]
		self.weight=doc["weight"]
		self.description=doc["description"]
		self.intuition=[]
		self.examples=[]
		self.notes=[]
		if "intuition" in doc:
			self.intuition=doc["intuition"]
		if "examples" in doc:
			for single_examples in doc["examples"]:
				self.examples.append(single_examples)
				
		if "notes" in doc:
			for single_notes in doc["notes"]:
				self.notes.append(single_notes)

	def __repr__(self):
		
		msg="(%s,%s,%s,%d)\n" %(self.name,self.type,self.description,self.weight)
		if self.intuition:
			msg=msg+self.intuition+"\n"
		for example in self.examples:
			msg=msg+example+"\n"
		
		return msg

	@property
	def name(self):
		return self.name

	@name.setter
	def name(self, new_name):
		self.name=new_name

	@property
	def type(self):
		return self.type

	@type.setter
	def type(self, newtype  ):
		if newtype is ('definition' or 'theorem' or 'exercise'):
			self.type = new_type
		else:
			warn('Bad type.')
	
	@property
	def weight(self):
		return self.weight
	
	@weight.setter
	def weight(self, new_weight):
		if isinstance(new_weight, (int, long, float)):
			self.weight=new_weight
		else:
			warn('Bad type')

	@property
	def description(self):
		return self.description
	
	@description.setter
	def description(self, new_description):
		self.description=new_description
	
	@property
	def intuition(self):
		return self.intuition

	@intuition.setter
	def intuition(self, new_intuition):
		self.intuition=new_intuition

	@property
	def examples(self):
		return self.examples

	@examples.setter
	def examples(self, example_overwrite):
		self.examples=[example_overwrite]

	def append_example(self, new_example):
		self.examples.append(new_example)

	@property
	def notes(self):
		return self.notes

	@notes.setter
	def notes(self, notes_overwrite):
		self.notes=[notes_overwrite]

	def append_note(self, new_note):
		self.notes.append(new_note)

	
	
	



def import_json(JsonDocumentFile):
	print("Importing from"+str(JsonDocumentFile))
	with open(JsonDocumentFile) as json_data:
		d=json.load(json_data)
		json_data.close()
	return d

	

if __name__=="__main__":

	print("Hello World")
	sample_theorem={"name":"Pythagorean theorem","type":"theorem","weight":1,"description":"a^2+b^2=c^2","intuition":"A simple explanation","examples":["Example 1","Example 2"]}
	sample_definition={"name":"triangle","type":"definition","weight":1,"description":"3 sided polygon","intuition":"A simple explanation","examples":["Example 1","Example 2"]}
	a=node(sample_theorem)
	b=node(sample_definition)
	print(a)
	print(b)
	# Importing the same documents from a file 
	json_data=import_json('JsonSample.txt')
	for x in json_data:
		c=node(x)
		print c
	

		









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
