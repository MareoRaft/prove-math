import re
from copy import deepcopy

from lib import helper
from lib.config import ERR
from lib.score import ScoreCard
from lib.decorate import read_only

def is_cclass(thing, cclass):
	# this could even be smarter, splitting by "of" and recursing down, if needed.
	if cclass in ['list of content str', 'list of str']:
		return isinstance(thing, list) and all([isinstance(el, str) for el in thing])
	elif cclass in ['list of dict']:
		return isinstance(thing, list) and all([isinstance(el, dict) for el in thing])
	else:
		return isinstance(thing, cclass)

def is_capitalized(value):
	if re.search(r'[\$A-Z]', value): # starts with LaTeX or capital letter
		return True
	return False

def score_string_content(score_card, value):
	if isinstance(value, list):
		for el in value:
			score_string_content(score_card, el)
	if isinstance(value, str):
		# this needs to know WHICH method is the called.  Description callers should get higher penalties, etc.
		if not len(value) >= 15: # arbitary length to make sure person actually put some content in
			score_card.strike("low-medium", ERR["LENGTH_TOO_SHORT"])
		if not is_capitalized(value):
			# we need to move this ONLY to the things that need to be capitalized (for example, not names)
			score_card.strike("low", ERR["NOT_CAPITALIZED"])


class Attr:


	def __init__(self, node=None, name=None, value=None, cclass=None, default="no default", setter=(lambda self, x: x)):
		self.node = node
		self.name = name
		self.cclass = cclass
		self.default = default
		self.setter = setter
		self.value = value

	@property
	def node(self):
		return self._node
	@node.setter
	@read_only
	def node(self, new_in):
		# we can't check if new_in is of the Node class because we would have to import Node, which is circular
		if not new_in:
			raise ValueError('empty node')
		self._node = new_in

	@property
	def name(self):
		return self._name
	@name.setter
	@read_only
	def name(self, new_in):
		if not isinstance(new_in, str) or not new_in:
			raise ValueError('bad name')
		self._name = new_in

	@property
	def setter(self):
		return self._setter
	@setter.setter
	def setter(self, new_in):
		# verify it can be called (like a function)
		assert callable(new_in)
		self._setter = new_in

	@property
	def cclass(self):
		return self._cclass
	@cclass.setter
	@read_only
	def cclass(self, new_in):
		# a list of allowed types, which can grow over time:
		ALLOWED_TYPES = [str, int, 'list of content str', 'list of str', 'list of dict']
		if new_in not in ALLOWED_TYPES:
			raise TypeError('type not yet permitted')
		self._cclass = new_in

	@property
	def value(self):
		return self._value
	@value.setter
	def value(self, new_in):
		# Reset the ScoreCard
		self.score_card = ScoreCard()

		# Set default
		if new_in is None:
			if self.default == "no default":
				if self.cclass in ['list of content str', 'list of str', 'list of dict']:
					new_in = list()
				else:
					new_in = self.cclass()
			else:
				new_in = self.default

		# Clean up shorthand inputs
		if isinstance(new_in, str) and self.cclass in [int]:
			new_in = self.cclass(new_in)
		if isinstance(new_in, str) and self.cclass in ['list of str', 'list of content str']:
			new_in = [new_in]
		if isinstance(new_in, dict) and self.cclass in ['list of dict']:
			new_in = [new_in]

		# Check type
		if not is_cclass(new_in, self.cclass):
			raise TypeError('Input value {} is not of class {}.  The Attr is {}.'.format(new_in, type(self.cclass()), self))

		# Clean any whitespace in strings
		if self.cclass in ('list of content str', 'list of str'):
			new_in = [string.strip() for string in new_in]
		elif self.cclass == str:
			new_in = new_in.strip()

		# Score strings as content if applicable
		if self.cclass == 'list of content str':
			score_string_content(self.score_card, new_in)

		# Set value
		self._value = self.setter(self, new_in)

	def as_dict(self):
		dic = {
			'name': self.name,
			'score_card': self.score_card.as_dict(),
		}

		# only if there is a value, show it too
		if hasattr(self, '_value'):
			dic['value'] = self.value

		return dic

	def __str__(self):
		return 'Attr{}'.format(self.as_dict())

