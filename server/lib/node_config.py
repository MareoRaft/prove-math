from copy import deepcopy

from lib.helper import reduce_string, remove_outer_dunderscores, dunderscore_count
from lib.config import ERR

# the type setter belongs to the node
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

# in the following setters, "self" is the attr object
# the following setters belong to the attr
def name_setter(self, new_name):
	if dunderscore_count(new_name) != 0:
		self.score_card.strike("critical", ERR["DUNDERSCORES_IN_NAME"](new_name))
	self.id = new_name
	return new_name

def theorem_name_setter(self, new_name):
	if self.name == '':
		self.score_card.strike("critical", ERR["NO_NAME"]) # maybe lower this if we can auto-assign a name
	return name_setter(self, new_name)

def importance_setter(self, new_importance):
	if new_importance < self.node.MIN_IMPORTANCE:
		self.score_card.strike("low", ERR["IMPORTANCE_TOO_LOW"](self, new_importance))
	new_importance = max(self.node.MIN_IMPORTANCE, new_importance)
	if new_importance > self.node.MAX_IMPORTANCE:
		self.score_card.strike("low", ERR["IMPORTANCE_TOO_HIGH"](self, new_importance))
	new_importance = min(self.node.MAX_IMPORTANCE, new_importance)
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

def negation_setter(self, new_negation):
	new_negation = remove_outer_dunderscores(new_negation)
	if dunderscore_count(new_negation) > 0:
		self.score_card.strike("medium", ERR["DUNDERSCORES"](new_negation))
	return new_negation

def definition_description_setter(self, new_description):
	if dunderscore_count(new_description) < 2:
		self.score_card.strike("low", ERR["NO_DUNDERSCORES"](new_description))
	return new_description

def pretheorem_description_setter(self, new_description):
	if dunderscore_count(new_description) != 0:
		self.score_card.strike("medium-high", ERR["DUNDERSCORES"](new_description))
	return new_description

def exercise_description_setter(self, new_in):
	if self.node.name == '':
		self.node.id = self.description
	return pretheorem_description_setter(self, new_in)

def axiom_dependencies_setter(self, new_deps):
	if new_deps:
		self.node.score_card.strike("medium", ERR["AXIOM_WITH_DEPENDENCY"])
	return new_deps


NODE_MIN_IMPORTANCE = 1
NODE_MAX_IMPORTANCE = 10

THEOREM_MIN_IMPORTANCE = 3

EXERCISE_MAX_IMPORTANCE = 3


NODE_ATTR_SETTINGS = {
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

DEFINITION_ATTR_SETTINGS = deepcopy(NODE_ATTR_SETTINGS)
DEFINITION_ATTR_SETTINGS.update({
	'plurals': {
		'keywords': ['plurals', 'plural', 'pl'],
		'ttype': 'list of str',
	},
	'negation': {
		'keywords': ['negation'],
		'ttype': str,
		'setter': negation_setter,
	},
})
DEFINITION_ATTR_SETTINGS['importance']['default'] = 4
DEFINITION_ATTR_SETTINGS['description']['setter'] = definition_description_setter

AXIOM_ATTR_SETTINGS = deepcopy(DEFINITION_ATTR_SETTINGS)
AXIOM_ATTR_SETTINGS['dependencies']['setter'] = axiom_dependencies_setter

PRETHEOREM_ATTR_SETTINGS = deepcopy(NODE_ATTR_SETTINGS)
PRETHEOREM_ATTR_SETTINGS['description']['setter'] = pretheorem_description_setter

THEOREM_ATTR_SETTINGS = deepcopy(PRETHEOREM_ATTR_SETTINGS)
THEOREM_ATTR_SETTINGS['importance']['default'] = 6
THEOREM_ATTR_SETTINGS['name']['setter'] = theorem_name_setter

EXERCISE_ATTR_SETTINGS = deepcopy(PRETHEOREM_ATTR_SETTINGS)
EXERCISE_ATTR_SETTINGS['importance']['default'] = 1
EXERCISE_ATTR_SETTINGS['description']['setter'] = exercise_description_setter
