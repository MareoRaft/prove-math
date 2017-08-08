from copy import deepcopy

from lib.helper import remove_outer_dunderscores, dunderscore_count, move_attribute
from lib.config import ERR

# the following setters are used by the attr
def name_setter(attr, new_name):
	if dunderscore_count(new_name) != 0:
		attr.score_card.strike("critical", ERR["DUNDERSCORES_IN_NAME"](new_name))
	return new_name

def theorem_name_setter(attr, new_name):
	if new_name == '':
		attr.score_card.strike("critical", ERR["NO_NAME"]) # maybe lower this if we can auto-assign a name
	return name_setter(attr, new_name)

def importance_setter(attr, new_importance):
	if new_importance < attr.node.MIN_IMPORTANCE:
		attr.score_card.strike("low", ERR["IMPORTANCE_TOO_LOW"](attr.node, new_importance))
	new_importance = max(attr.node.MIN_IMPORTANCE, new_importance)
	if new_importance > attr.node.MAX_IMPORTANCE:
		attr.score_card.strike("low", ERR["IMPORTANCE_TOO_HIGH"](attr.node, new_importance))
	new_importance = min(attr.node.MAX_IMPORTANCE, new_importance)
	return new_importance

def list_of_content_setter(attr, new_things):
	for x in new_things:
		if dunderscore_count(x) > 0:
			attr.score_card.strike("low", ERR["DUNDERSCORES"](x))
	return new_things

def dependencies_setter(attr, new_dependencies):
	new_dependencies = [remove_outer_dunderscores(d) for d in new_dependencies]
	for d in new_dependencies:
		if dunderscore_count(d) > 0:
			attr.score_card.strike("critical", ERR["DUNDERSCORES"](d))
	return new_dependencies

def negation_setter(attr, new_negation):
	new_negation = remove_outer_dunderscores(new_negation)
	if dunderscore_count(new_negation) > 0:
		attr.score_card.strike("medium", ERR["DUNDERSCORES"](new_negation))
	return new_negation

def definition_description_setter(attr, new_description):
	if dunderscore_count(new_description) < 2:
		attr.score_card.strike("low", ERR["NO_DUNDERSCORES"](new_description))
	return new_description

def pretheorem_description_setter(attr, new_description):
	if dunderscore_count(new_description) != 0:
		attr.score_card.strike("medium-high", ERR["DUNDERSCORES"](new_description))
	return new_description

def axiom_dependencies_setter(attr, new_deps):
	if new_deps:
		attr.score_card.strike("medium", ERR["AXIOM_WITH_DEPENDENCY"])
	return new_deps

def proofs_setter(attr, new_proofs):
	assert isinstance(new_proofs, list)
	for proof in new_proofs:
		proof['description'] = move_attribute(proof, {'description', 'content'}, strict=True)
		if dunderscore_count(proof['description']) > 0:
			attr.score_card.strike("low", ERR["DUNDERSCORES"](proof['description']))
		if 'type' not in proof:
			attr.score_card.strike("low", ERR["NO_PROOF_TYPE"])
			# then give some default type to the proof
			proof['type'] = []
		else:
			if isinstance(proof['type'], str):
				proof['type'] = [proof['type']]
		# proof['type'] = check_type_and_clean(proof['type'], str, list_of=True) # we could really use a deep type checker for python, like what check.types has: check.is.array.of.string(thing)
	return new_proofs


NODE_MIN_IMPORTANCE = 1
NODE_MAX_IMPORTANCE = 10

THEOREM_MIN_IMPORTANCE = 3

EXAMPLE_MAX_IMPORTANCE = 7

EXERCISE_MAX_IMPORTANCE = 3


NODE_ATTR_SETTINGS = {
	'preamble': {
		'keywords': ['preamble'],
		'cclass': str,
		'default': 'Put your $\LaTeX$ macros for the node here.  Remember to wrap them in \$\'s!',
	},
	'number': {
		'keywords': ['number', 'num'],
		'cclass': str,
	},
	'name': {
		'keywords': ['name'],
		'cclass': str,
		'setter': name_setter,
	},
	'examples': {
		'keywords': ['example', 'examples'],
		'cclass': 'list of content str',
		'setter': list_of_content_setter,
	},
	'counterexamples': {
		'keywords': ['counterexample', 'counterexamples', 'counter example', 'counter examples'],
		'cclass': 'list of content str',
		'setter': list_of_content_setter,
	},
	'importance': {
		'keywords': ['importance', 'weight'],
		'cclass': int,
		'default': -1,
		'setter': importance_setter,
	},
	'description': {
		'keywords': ['description', 'content', 'descriptions', 'contents'],
		'cclass': str,
	},
	'intuitions': {
		'keywords': ['intuitions', 'intuition'],
		'cclass': 'list of content str',
		'setter': list_of_content_setter,
	},
	'notes': {
		'keywords': ['note', 'notes'],
		'cclass': 'list of content str',
		'setter': list_of_content_setter,
	},
	'dependencies': {
		'keywords': ['dependencies', 'dependency'],
		'cclass': 'list of str',
		'setter': dependencies_setter,
	},
}

DEFINITION_ATTR_SETTINGS = deepcopy(NODE_ATTR_SETTINGS)
DEFINITION_ATTR_SETTINGS.update({
	'plurals': {
		'keywords': ['plurals', 'plural', 'pl'],
		'cclass': 'list of str',
	},
	'negation': {
		'keywords': ['negation'],
		'cclass': str,
		'setter': negation_setter,
	},
})
DEFINITION_ATTR_SETTINGS['importance']['default'] = 4
DEFINITION_ATTR_SETTINGS['description']['setter'] = definition_description_setter

AXIOM_ATTR_SETTINGS = deepcopy(DEFINITION_ATTR_SETTINGS)
AXIOM_ATTR_SETTINGS['dependencies']['setter'] = axiom_dependencies_setter

proofs_dict = {
	'keywords': ['proofs', 'proof'],
	# 'cclass': 'list of dict', for the semester, proofs will just be a list of content
	'cclass': 'list of content str',
	# 'setter': proofs_setter, for the semester, proofs will just be a list of content
	'setter': list_of_content_setter,
}

EQUIV_DEFS_SETTINGS = deepcopy(DEFINITION_ATTR_SETTINGS)
EQUIV_DEFS_SETTINGS.update({
	'proofs': proofs_dict,
})

PRETHEOREM_ATTR_SETTINGS = deepcopy(NODE_ATTR_SETTINGS)
PRETHEOREM_ATTR_SETTINGS.update({
	'proofs': proofs_dict,
})
PRETHEOREM_ATTR_SETTINGS['description']['setter'] = pretheorem_description_setter

THEOREM_ATTR_SETTINGS = deepcopy(PRETHEOREM_ATTR_SETTINGS)
THEOREM_ATTR_SETTINGS['importance']['default'] = 6
THEOREM_ATTR_SETTINGS['name']['setter'] = theorem_name_setter

EXAMPLE_ATTR_SETTINGS = deepcopy(THEOREM_ATTR_SETTINGS)
EXAMPLE_ATTR_SETTINGS['importance']['default'] = 2

EXERCISE_ATTR_SETTINGS = deepcopy(PRETHEOREM_ATTR_SETTINGS)
EXERCISE_ATTR_SETTINGS['importance']['default'] = 1
