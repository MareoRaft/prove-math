javascript_kickoff_file = 'config'

starting_nodes = {
	'graph theory': ['set', 'multiset', 'vertex'],
	'combinatorics': ['set', 'multiset', 'identical', 'factorial', 'finiteset'],
	'category theory': ['equatable', 'type'],
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

'subject': 'combinatorics',
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
