import re
from copy import deepcopy

from lib import helper
from lib.config import ERR
from lib.score import ScoreCard
from lib.decorate import read_only
from lib.score import ScoreCard

def is_type(thing, ttype):
	# this could even be smarter, splitting by "of" and recursing down, if needed.
	if ttype in ('list of content str', 'list of str'):
		return isinstance(thing, list) and all([isinstance(el, str) for el in thing])
	else:
		return isinstance(thing, ttype)

def string_to_bool(string):
	string = string.lower()
	if string == "true":
		return True
	elif string == "false":
		return False
	else:
		raise ValueError('Cannot convert string to bool.')

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


	def __init__(self, name=None, value=None, ttype=None, required=False, default="no default", setter=(lambda x: x), score_content=False):
		self.name = name
		self.ttype = ttype
		self.required = required
		self.default = default
		self.setter = setter
		self.value = value

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
	def required(self):
		return self._required
	@required.setter
	@read_only
	def required(self, new_in):
		if isinstance(new_in, str):
			new_in = string_to_bool(new_in)
		assert isinstance(new_in, bool)
		self._required = new_in

	@property
	def ttype(self):
		return self._ttype
	@ttype.setter
	@read_only
	def ttype(self, new_in):
		# a list of allowed types, which can grow over time:
		ALLOWED_TYPES = [str, int, 'list of content str', 'list of str']
		if new_in not in ALLOWED_TYPES:
			raise TypeError('type not yet permitted')
		self._ttype = new_in

	@property
	def value(self):
		return self._value
	@value.setter
	def value(self, new_in):
		# Reset the ScoreCard
		self.score_card = ScoreCard()

		# Set default
		if new_in is None:
			if self.default != "no default":
				new_in = self.default
			else:
				new_in = self.ttype()

		# Clean up shorthand inputs
		if isinstance(new_in, str) and self.ttype in [int]:
			new_in = self.ttype(new_in)
		if isinstance(new_in, str) and self.ttype in ['list of str', 'list of content str']:
			new_in = list(new_in)

		# Check type
		assert is_type(new_in, self.ttype)

		# Clean any whitespace in strings
		if self.ttype in ('list of content str', 'list of str'):
			new_in = [string.strip() for string in new_in]
		elif self.ttype == str:
			new_in = new_in.strip()

		# Score strings as content if applicable
		if self.ttype == 'list of content str':
			score_string_content(self.score_card, new_in)

		# Set value
		self._value = self.setter(new_in)

