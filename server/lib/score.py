from copy import deepcopy

FAILING_SCORE = 40

SEVERITY_WORD_TO_NUMBER = {
	"low": 5,
	"medium": 10,
	"high": 20,
	"critical": FAILING_SCORE,
}

def severity_string_to_number(string):
	assert isinstance(string, str)
	words = string.split("-")
	numbers = [SEVERITY_WORD_TO_NUMBER[word] for word in words]
	number = sum(numbers) / len(numbers) # the average severity
	return number


class ScoreCard:


	def __init__(self):
		# a stack of strikes
		self.strikes = []

	def strike(self, severity_string, message):
		severity_number = severity_string_to_number(severity_string)
		self.strikes.append((severity_number, message))

	def total_score(self):
		scores = [report[0] for report in self.strikes]
		return sum(scores)
		# why is my score 0?  Well, since there is no description, it didn't even attempt to set a descruption in the first place.  Maybe the description should be an EMPTY STRING instead of not setting one.  Or maybe some smarter way?

	def is_passing(self):
		return self.total_score() < FAILING_SCORE

	def as_dict(self):
		dic = deepcopy(self.__dict__)
		# make sure d.strikes is nice
		# make sure is_passing is nice
		# delete unneeded keys
		return dic

	def extend(self, score_card):
		self.strikes.extend(score_card.strikes)
