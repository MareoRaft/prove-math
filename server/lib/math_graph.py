import networkx as nx

from lib.pmdag import PMDAG
from lib.decorate import record_elapsed_time
from lib.config import starting_nodes


class MathGraph (PMDAG):
	""" Prove Math specific graph methods for the user go here, e.g. anything using our custom user objects. """


	# FROM GRAPH
	# (nothing)

	# FROM DIGRAPH
	def unlearned_dependency_tree(self, user, target):
		learned_nodes = user.dict['learned_node_ids']
		return self.unselected_dependency_tree(target, learned_nodes)

	def learn_count(self, user, target):
		learned_nodes = user.dict['learned_node_ids']
		return self.unselected_count(target, learned_nodes)

	def learn_counts(self, user, target_bunch):
		learned_nodes = user.dict['learned_node_ids']
		return self.unselected_counts(target_bunch, learned_nodes)

	# FROM DAG:
	def learnable_successors(self, user):
		learned_nodes = user.dict['learned_node_ids']
		return self.absolute_dominion(learned_nodes)

	def choose_goal(self, user):
		"""
		:returns: One immediate successor to learned_nodes which we should set as the new goal (chosen by depth, then learn count, then importance, then id).
		"""
		subject = user.dict['prefs']['subject']
		axioms = starting_nodes[subject]
		learned_nodes = user.dict['learned_node_ids']

		return self.choose_destination(axioms, learned_nodes)

	def learnable_pregoals(self, user, goal):
		learned_nodes = user.dict['learned_node_ids']
		return self.predestinations(goal, learned_nodes)

	def choose_learnable_pregoals(self, user, number=None):
		subject = user.dict['prefs']['subject']
		axioms = starting_nodes[subject]
		learned_nodes = user.dict['learned_node_ids']
		if not number:
			number = user.dict['prefs']['send_learnable_pregoal_number']
		goal = user.dict['prefs']['goal_id']

		return self.choose_selectable_predestinations(axioms, learned_nodes, number=number, destination=goal)

	@record_elapsed_time
	def nodes_to_send(self, user, client_node_ids=[]):
		learned_ids = user.dict['learned_node_ids']
		pref = user.dict['prefs']

		ids_to_send = set()

		# nodes to send no matter what:
		if not pref['subject']:
			# the User class initialization should guarantee we don't hit this line unless something resets subject to None:
			raise ValueError("User's subject has been deleted!")
		if not pref['subject'] in starting_nodes.keys():
			# not a valid subject choice
			raise ValueError("User's subject was somehow set to an invalid choice!")

		if pref['sticky_client_nodes']:
			ids_to_send.update(client_node_ids)
		# else:
		# we might want to think about how we want these to behave with sticky nodes.
		# for now, always send.
		ids_to_send.update(starting_nodes[pref['subject']])
		ids_to_send.update(learned_ids)

		# learnable nodes to send based on preference:
		if pref['always_send_learnable_successors']:
			ids_to_send.update(self.learnable_successors(user))

		if pref['always_send_learnable_pregoals']:
			ids_to_send.update(self.choose_learnable_pregoals(user))

		if pref['requested_pregoal_id']:
			ids_to_send.add(pref['requested_pregoal_id'])

		# nodes related to the user's goal:
		if pref['goal_id']:
			if pref['always_send_goal']:
				ids_to_send.add(pref['goal_id'])
			if pref['always_send_unlearned_dependency_tree_of_goal']:
				ids_to_send.update(self.unlearned_dependency_tree(user, pref['goal_id']))

		return ids_to_send

