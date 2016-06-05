""" A Vote object is a timestamp of when the vote was cast, and whether it was an upvote or a downvote. """
from datetime import datetime

from lib.decorate import read_only


class Vote:


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

