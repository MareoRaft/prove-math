from datetime import datetime

from lib.decorate import read_only


class Votable:
	"""A Votable object is an object that people can casts votes on.  The votes are recorded in self._votes.  Votable has no __init__ because it's purpose is to be inherited by other objects that we want to become votable.  Those objects will have their own __init__s, and should include the line `self._votes = []` in their __init__."""


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


class Vote:
	""" A Vote object is a timestamp of when the vote was cast, and whether it was an upvote or a downvote. """


	def __init__(self, kind, date=None):
		self.kind = kind
		self.date = date

	@property
	def kind(self):
		return self._kind
	@kind.setter
	def kind(self, new_kind):
		if new_kind in {'up', 'down'}:
			self._kind = new_kind
		else:
			raise Exception('Bad Vote kind.')

	def is_up(self):
		return self.kind == 'up'

	def is_down(self):
		return not self.is_up()

	def parity(self):
		if self.is_up():
			return 1
		else:
			return -1

	@property
	def date(self):
		return self._date
	@date.setter
	@read_only
	def date(self, new_date):
		# convert JS dates to datetime objects?
		if isinstance(new_date, datetime):
			self._date = new_date
		else:
			raise Exception('Date is not of type datetime.')

	def weight(self):
		return 1
		# in the future, we want the weight to decrease as the date gets older
		# now = datetime.utcnow()
		# elapsed_time = now - self
		# return log_decay(elapsed_time)

