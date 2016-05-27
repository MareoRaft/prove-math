import networkx as nx
from lib.networkx.classes import dag # attaches DAG to nx

from lib.decorate import record_elapsed_time
from lib.config import starting_nodes


class MathGraph (nx.DAG):
	""" Prove Math specific graph methods go here, e.g. anything using our custom node or user objects. """


	# FROM GRAPH:
	def n(self, node_id):
		return self.node[node_id]["custom_object"]

	def add_n(self, nodebunch):
		if not self.acceptable_iterable(nodebunch): # nodebunch must be a single node
			nodebunch = [nodebunch]
		for node in nodebunch:
			self.add_node(node.id, attr_dict={"custom_object": node})

	# FROM DIGRAPH:
	def as_js_ready_dict(self):
		d = dict()
		d['nodes'] = [self.n(node_id).__dict__ for node_id in self.nodes()]
		d['links'] = [{'source': source, 'target': target} for (source, target) in self.edges()]
		return d

	# @record_elapsed_time
	def unlearned_dependency_tree(self, target, learned_nodes):
		if not self.acceptable_iterable(learned_nodes):
			raise ValueError('Argument {} is not iterable'.format(learned_nodes))
		DG = self.copy()
		DG.remove_nodes_from(learned_nodes)
		return nx.ancestors(DG, target).union({target})

	def learn_count(self, target, learned_nodes):
		return len(self.unlearned_dependency_tree(target, learned_nodes))

	def learn_counts(self, target_bunch, learned_nodes):
		if not self.acceptable_iterable(learned_nodes):
			raise ValueError('Argument {} is not iterable'.format(learned_nodes))
		DG = self.copy()	# lets us bypass calling unlearned_dependency_tree repeatedly
		DG.remove_nodes_from(learned_nodes)
		return [len(DG.ancestors(target).union({target})) for target in target_bunch]

	# FROM DAG:
	# @record_elapsed_time
	def importance_weight(self, node):
		distance_from_node = 0
		current_depth_nodes = {node}
		already_counted_nodes = set() # needed in case there are any cycles
		predecessors = {node}
		successors = {node}	#kept separate because descendants are given more weight than ancestors in asessing a node's importance
		ANCESTORS_DESCENDANTS_WEIGHT_FRACTION = 1/6
		NEIGHBOR_NORMALIZATION_FRACTION = 1/10 #rescales the sum of all neighbor importances to match the scale of the original node's own importance, i.e. [1,10]
		EXPECTED_NEIGHBORS_PER_NODE = 3

		norm_importances = [self.n(node).importance] #normalized importance of the nodes in each depth level
		SEARCH_DEPTH_LIMIT = 4
		while distance_from_node < SEARCH_DEPTH_LIMIT:
			distance_from_node += 1
			if predecessors:
				predecessors = self.predecessors(predecessors) - already_counted_nodes	#needed in case there are any cycles
			else:
				predecessors = set()
			if successors:
				successors = self.successors(successors) - already_counted_nodes
			else:
				successors = set()
			if (len(successors) + len(predecessors)) == 0:	#no more neighbors, don't look any further
				norm_importances.append(0)
				break
			predecessors_importances = [ANCESTORS_DESCENDANTS_WEIGHT_FRACTION * self.n(n).importance for n in predecessors]
			successors_importances = [(1-ANCESTORS_DESCENDANTS_WEIGHT_FRACTION) * self.n(n).importance for n in successors]	#weighted toward descendants
			current_depth_importances = predecessors_importances + successors_importances

			current_depth_normalized_sum = sum(current_depth_importances) * NEIGHBOR_NORMALIZATION_FRACTION / (EXPECTED_NEIGHBORS_PER_NODE**distance_from_node)
			#As distance increases there are exponentially more neighbors.  The 1/(EXPECTED_NEIGHBORS_PER_NODE**distance) term counteracts this.
			norm_importances.append(current_depth_normalized_sum)

			already_counted_nodes = already_counted_nodes.union(predecessors)
			already_counted_nodes = already_counted_nodes.union(successors)
		weighted_importances = [(importance/(index+1)**2) for index, importance in enumerate(norm_importances)]	#normalized importance of the nodes in each depth level, weighted against distance from node
		neighbors_weight = sum(weighted_importances)
		return neighbors_weight #(neighbors_weight, self.n(node).id)

	# @record_elapsed_time
	def most_important(self, nbunch, number=1):
		def most_important_sorter(node):
			return (self.importance_weight(node), self.n(node).id)
		if number <= 0:
			raise ValueError('Must give number > 0')
		if len(nbunch) < number:
			raise ValueError('Asked for more nodes than you provided')
		nodes_by_importance = sorted(nbunch, key=most_important_sorter, reverse=True)
		return nodes_by_importance[:number]

	# @record_elapsed_time
	def choose_goal(self, *args, user=None):	# short sighted, depth-first
		"""
		:returns: One immediate successor to learned_nodes which we should set as the new goal (chosen by depth, then learn count, then importance, then id).
		"""
		if user is None:
			axioms = args[0]
			learned_nodes = args[1]
		else:
			subject = user.dict['prefs']['subject']
			axioms = starting_nodes[subject]
			learned_nodes = user.dict['learned_node_ids']

		self.validate_input_nodes(axioms)
		self.validate_input_nodes(learned_nodes)
		# if the use has learned nothing, emit an error
		if not learned_nodes:
			raise Exception('User must choose a subject and learn one of the starting nodes before choosing a goal.')

		depth_to_successors_dict = self.depth_to_successors_dict(axioms, learned_nodes)
		deepest_successors = list(depth_to_successors_dict.items())[0][1]
		if not deepest_successors:
			# no more successors.  the user has finished the subject and needs to choose a new one
			return None

		# Now sort the deepest successors by learn count, then by importance, and finally name to break a tie.
		# If we need better efficiency, use DiGraph.learn_counts(targets, learned_nodes)
		def learn_count_sorter(successor):
			return (
				self.learn_count(successor, learned_nodes),
				-self.importance_weight(successor),
				self.n(successor).id,
			)
		goal = sorted(deepest_successors, key=learn_count_sorter)[0]
		return goal

	# @record_elapsed_time
	def learnable_pregoals(self, goal, learned_nodes):	# a pregoal is an unlearned dependency of the goal, or the goal itself
		learnable_nodes = set(self.absolute_dominion(learned_nodes)).union(self.sources())
		pregoals = self.unlearned_dependency_tree(goal, learned_nodes)
		return set.intersection(learnable_nodes, pregoals)

	# @record_elapsed_time
	def choose_learnable_pregoals(self, *args, user=None, **kwargs):
		if user is None:
			axioms = args[0]
			learned_nodes = args[1]
			if 'number' in kwargs:
				number = kwargs['number']
			else:
				number = 1
			if 'goal' in kwargs:
				goal = kwargs['goal']
			else:
				goal = None
		else:
			subject = user.dict['prefs']['subject']
			axioms = starting_nodes[subject]
			learned_nodes = user.dict['learned_node_ids']
			number = user.dict['prefs']['send_learnable_pregoal_number']
			goal = user.dict['prefs']['goal_id']

		if goal is None:
			goal = self.choose_goal(axioms, learned_nodes)
		learnable_pregoals = self.learnable_pregoals(goal, learned_nodes)
		return self.most_important(learnable_pregoals, number)

	# @record_elapsed_time
	def nodes_to_send(self, user=None):
		if user is None:
			raise ValueError("Did not give a user!")

		learned_ids = user.dict['learned_node_ids']
		ids_to_send = set()
		pref = user.dict['prefs']
		subject = pref['subject']
		goal_id = pref['goal_id']

		# nodes to send no matter what:
		if not subject:
			# the User class initialization should guarantee we don't hit this line unless something resets subject to None:
			raise ValueError("User's subject has been deleted!")
		if not subject in starting_nodes.keys():
			# not a valid subject choice
			raise ValueError("User's subject was somehow set to an invalid choice!")
		ids_to_send.update(starting_nodes[subject])
		ids_to_send.update(learned_ids)

		# learnable nodes to send based on preference:
		if pref['always_send_absolute_dominion'] and learned_ids:
			ids_to_send.update(self.absolute_dominion(learned_ids))

		if pref['always_send_learnable_pregoals'] and learned_ids:
			axioms = starting_nodes[subject]
			pregoals = self.choose_learnable_pregoals(user=user)
			ids_to_send.update(pregoals)

		if pref['requested_pregoal_id']:
			ids_to_send.add(pref['requested_pregoal_id'])

		# nodes related to the user's goal:
		if goal_id:
			if pref['always_send_goal']:
				ids_to_send.add(goal_id)
			if pref['always_send_unlearned_dependency_tree_of_goal']:
				ids_to_send.update(self.unlearned_dependency_tree(goal_id, learned_ids))

		return ids_to_send # could just return self.subgraph(list(ids_to_send)) but this makes testing simpler

