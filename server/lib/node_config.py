from lib.helper import reduce_string, remove_outer_dunderscores, dunderscore_count
from lib.config import ERR

def type_setter(new_type):
	if new_type in {'definition', 'defn', 'def'}:
		return 'definition'
	elif new_type in {'axiom'}:
		return 'axiom'
	elif new_type in {'theorem', 'thm'}:
		return 'theorem'
	elif new_type in {'exercise'}:
		return 'exercise'
	else:
		raise TypeError(ERR["BAD_TYPE"](new_type))

def name_setter(new_name):
	if dunderscore_count(new_name) != 0:
		self.score_card.strike("critical", ERR["DUNDERSCORES_IN_NAME"](new_name))
	self.id = new_name
	return new_name

def importance_setter(self, new_importance):
	if new_importance < self.MIN_IMPORTANCE:
		self.score_card.strike("low", ERR["IMPORTANCE_TOO_LOW"](self, new_importance))
	new_importance = max(self.MIN_IMPORTANCE, new_importance)
	if new_importance > self.MAX_IMPORTANCE:
		self.score_card.strike("low", ERR["IMPORTANCE_TOO_HIGH"](self, new_importance))
	new_importance = min(self.MAX_IMPORTANCE, new_importance)
	return new_importance

def list_of_content_setter(self, new_things):
	for x in new_things:
		if dunderscore_count(x) > 0:
			self.score_card.strike("low", ERR["DUNDERSCORES"](x))
	return new_things

def dependencies_setter(self, new_dependencies):
	new_dependencies = [remove_outer_dunderscores(d) for d in new_dependencies]
	for d in new_dependencies:
		if dunderscore_count(d) > 0:
			self.score_card.strike("critical", ERR["DUNDERSCORES"](d))
	return new_dependencies

ATTR_DICT = {
	'type': {
		'ttype': str,
		'setter': type_setter
	},
	'id': {
		'ttype': str,
		'setter': reduce_string,
	},
	'name': {
		'keywords': ['name'],
		'ttype': str,
		'setter': name_setter,
	},
	'examples': {
		'keywords': ['example', 'examples'],
		'ttype': 'list of content str',
		'setter': list_of_content_setter,
	},
	'counterexamples': {
		'keywords': ['counterexample', 'counterexamples', 'counter example', 'counter examples'],
		'ttype': 'list of content str',
		'setter': list_of_content_setter,
	},
	'importance': {
		'keywords': ['importance', 'weight'],
		'ttype': int,
		'default': -1,
		'setter': importance_setter,
	},
	'description': {
		'keywords': ['description', 'content', 'descriptions', 'contents'],
		'ttype': 'list of content str',
	},
	'intuitions': {
		'keywords': ['intuitions', 'intuition'],
		'ttype': 'list of content str',
		'setter': list_of_content_setter,
	},
	'notes': {
		'keywords': ['note', 'notes'],
		'ttype': 'list of content str',
		'setter': list_of_content_setter,
	},
	'dependencies': {
		'keywords': ['dependencies', 'dependency'],
		'ttype': 'list of str',
		'setter': dependencies_setter,
	},
}
