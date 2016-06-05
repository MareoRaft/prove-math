""" A Node basically has a dictionary of attributes.  Each attribute has a key and a value (aka Atom).

For example, the node "vertex" has an attribute whose key is "definition" and whose Atom a has the following:
a.value = "A __vertex__ is a fundamental unit of a graph."
a.upvotes = 5
a.downvotes = 1
a.score = 4
"""


class Atom:


	def __init__(self, value):
		self.value = value
		self._votes = []

	def votes(self):
		""" Returns the list of Vote objects, in chronological order by their date. """
		return self._votes

	def add_vote(self, vote):
		""" Insert the new vote into the list of Vote objects, maintaining chronlogical order by date. """
		for old_vote in reversed(self.votes()):
			if old_vote.date < vote.date:
				# insert vote immediately after old_vote
				return
		# insert vote at very beginning

	def upvotes(self):
		""" Return the number of upvotes this Atom has. """
		upvote_list = [vote for vote in self.votes() if vote.is_up()]
		return len(upvote_list)

	def downvotes(self):
		# same
		pass

	def score(self):
		""" Calculate the Atom's score based on its votes. """
		score_list = [vote.parity() * vote.weight() for vote in self.votes()]
		return sum(score_list)

