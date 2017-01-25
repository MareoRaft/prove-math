javascript_kickoff_file = 'config'

LINEAR_ALGEBRA = ['rank', 'a'] # soon: null space, row space, matrix, etc
ABSTRACT_ALGEBRA = ['set', 'magma', 'composition']
MULTIVARIABLE_CALCULUS = ['tangent plane', 'directional derivative', 'homeomorphism']
starting_nodes = {
	'test': ['a'],
	'graph theory': ['set', 'multiset', 'vertex'],
	'combinatorics': ['set', 'multiset', 'identical', 'factorial', 'finiteset'],
	'category theory': ['equatable', 'type'],
	'l': LINEAR_ALGEBRA,
	'linear algebra': LINEAR_ALGEBRA,
	'abstract algebra': ABSTRACT_ALGEBRA,
	'algebra': ABSTRACT_ALGEBRA,
	'multivariable calculus': MULTIVARIABLE_CALCULUS,
	'multivariable calc': MULTIVARIABLE_CALCULUS,
	'calculus': MULTIVARIABLE_CALCULUS,
	'calc': MULTIVARIABLE_CALCULUS,
	'differential topology': ['n-sphere', 'tangent bundle'],
	'a': ['endomorphismgroupofmodules', 'isomorphismtheoremformodules', '3111example', 'indecomposable', 'leftrmodule', 'kernelofamodulemorphism', 'remarkson3112', 'corollaryof316', 'quotientmodule', 'homgroupofmodules', '3112example', 'examplesofprevious', 'consequencesofannihilator', 'rmodulemorphism', 'submodule', 'generate', 'internaldirectsum', 'annihilator', 'leftrmoduleconsequences', 'consequencesofrlinear'],
}

DEF_USER_PREFS = {
'display_name_capitalization': None,
# :description: This controls the capitalization of node titles.
# :possible values:
# None -- No capitalization is added.
# "sentence" -- The first letter is capitalized.
# "title" -- The first letter of every important word is capitalized.
# Be aware that people's last names, such as 'Euler', will always be capitalized.

'definition_decoration': "underline",
# :description: When a term is first defined (in its definition node), apply decoration to that term.
# :possible values: "underline", "italic", "bold", None

'show_description_on_hover': False,
# :description: When you hover your mouse over a node in the graph animation, the main description of the node will appear.
# :type: bool

'restrict_to_subject': False,
# :description: User can only get nodes within the subject.
# :type: bool

'enforce_learn_order': True,
# :description: User can only learn things in order (with exception of starting nodes).  That is, they can ONLY learn LEARNABLE nodes.
# :possible values: True, False, or "flexible" (allows user to override when they really want to)

'subject': 'graph theory',
# :description: The current subject that the user is studying.
# :possible values: any key of the starting_nodes dictionary in config.py

'goal_id': None,
# :description: User can choose a goal (the goal is a node) to work toward.  This can also be set by calling choose_goal.  This will be used by choose_learnable_pregoals.
# :type: string (must be an existing node id)

'requested_pregoal_id': None,
# :description: This should only be set when the user asks for a pregoal.  It is separate from the automatically chosen pregoals from always_send_learnable_pregoals.
# :type: string (must be an existing node id)

'always_send_learnable_successors': True,
# :description: Always send nodes that (user is capable of learning AND are successors of what they've already learned).
# :type: bool

'always_send_learnable_pregoals': True,
# :description: Always send *number* (see below) of nodes that the user is capable of learning and works towards their designated (or automatically chosen) goal.
# :type: bool

'send_learnable_pregoal_number': 1,
# :description: The NUMBER of learnable pregoals to send whenever we send learnable pregoals over.
# :possible values: natural number 1 or more

'always_send_goal': False,
# :description: Displays the user's goal in the client graph, even if it is not yet learnable.
# :type: bool

'always_send_unlearned_dependency_tree_of_goal': False,
# :description: Displays the entire unlearned dependency tree of the user's goal, including pregoals which are not yet learnable.
# :type: bool

'always_accept_suggested_goal': False,
# :description: When the user asks for a goal suggestion, the first suggestion given is automatically accepted as the user's new goal.
# :type: bool

'always_accept_suggested_pregoal': False,
# :description: When the user asks for a pregoal suggestion, the first suggestion given is automatically accepted as the user's new pregoal.
# :type: bool

'sticky_client_nodes': False,
# :description: User will always receive every node already included in the client graph.  Nodes will not be removed.
# :type: bool
}

ERR = {
# warnings and error messages for users

# bad type
"BAD_TYPE": (lambda x: "Node's 'type' attribute must be a 'definition' (or 'defn' or 'def'), a 'theorem' (or 'thm'), or an 'exercise'.\nYOUR TYPE WAS: {}".format(x)),

# complain that there are NO DUNDERSCORES
"NO_DUNDERSCORES": (lambda x: "The pattern __ should be used in your string to underline the new term that you are defining.  Your string is: {}".format(x)),

# complain that DUNDERSCORES exist
"DUNDERSCORES": (lambda x: "The pattern __ is not recommended in your string.  The pattern __ is reserved for underlining a term the very first time it is defined.  Your string is: {}".format(x)),

# names can't have dunderscores
"DUNDERSCORES_IN_NAME": (lambda x: "The pattern __ is not allowed in a name.  Your name is: {}".format(x)),

# complain that there is no name
"NO_NAME": "Your new node needs a name!  Please provide a name at the top in the name field.  For definitions, there is an alternative way to provide a name.  Simply surround the __new term__ in double underscores in the description.  For definitions, this is recommended.",

# complain that an axiom has a dependency
"AXIOM_WITH_DEPENDENCY": "You are trying to create an axiom that has a dependency.  This is allowed, but please make sure you know what you are doing.  Axioms are important!",

"NO_PROOF_TYPE": "You have not given your proof a type.  While not required, it can be useful to tag proofs with types, such as 'induction', 'combinatorial', 'algebraic', 'extremal', 'direct', 'contradiction', etc.",

"IMPORTANCE_TOO_LOW": (lambda node, importance: "The minimum importance for a {} node is {}.  The importance you set was {}.  This value will be replaced with the minimum importance.".format(node.type, node.MIN_IMPORTANCE, importance)),

"IMPORTANCE_TOO_HIGH": (lambda node, importance: "The maximum importance for a {} node is {}.  The importance you set was {}.  This value will be replaced with the maximum importance.".format(node.type, node.MAX_IMPORTANCE, importance)),

"LENGTH_TOO_SHORT": "The length of your content is too short (add more later).",

"NOT_CAPITALIZED": "Please capitalize the first letter of your first sentence.",
}



