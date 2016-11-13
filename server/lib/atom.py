""" A Node basically has a dictionary of attributes.  Each attribute has a key and a value (aka Atom).

For example, the node "vertex" has an attribute whose key is "definition" and whose Atom a has the following:
a.value = "A __vertex__ is a fundamental unit of a graph."
a.upvotes = 5
a.downvotes = 1
a.score = 4
"""
from lib.vote import Votable


class Atom (Votable):
	""" Yes, this class really is that short. """


	def __init__(self, value):
		self.value = value
		self._votes = []


