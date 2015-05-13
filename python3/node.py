# I would like to make a python3 script which uses this class and allows me to manually input new definitions, theorems, lemmas, etc.

from warnings import warn

class node:

	def __init__(self, dictionary):
		for key in dictionary:
			if key is in keys of translation hash:
				translate it to the value
			if key is 'definition':
				self.definition = dictionary[key]
			else if key is 'theorem':
				j
			else if ...
			else
				warn('Unidentified key.')


	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):
		if type is ('definition' or 'theorem' or 'exercise'):
			self.__type = type
		else:
			warn('Bad type.')


	@property
	def definition(self):
		return self.__definition

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

