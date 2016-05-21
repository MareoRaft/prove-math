from lib import clogging
log = clogging.getLogger('main')
from lib.mongo import Mongo


class User: # there's really no point in storing users ephemerally, other than to associate a specific user with a specific websocket


	USERS = Mongo("provemath", "users")

	def __init__(self, initial_identifier):
		log.debug('inital ident: '+str(initial_identifier))
		if initial_identifier['type'] in ['google', 'facebook', 'github', 'linkedin', 'local']:
			self.account_type = initial_identifier['type']
			self.account_id = initial_identifier['id']
			self.logged_in = (initial_identifier['type'] != 'local')
		else:
			raise Exception('Bad account type.')

		if self.account_id is None:
			self.account_id = self._unique_local_id()

		# check if they are in database.  if not, add them!
		if not self._get_from_db():
			self._set_to_db()

	def _get_from_db(self): # doubles as is_in_db, since it is True for that and False otherwise
		# This method is INTERNAL because it doesn't clean out the _id like .dict() does.
		user_dicts = list(self.USERS.find(self._mongo_identifier_dict()))
		if len(user_dicts) > 1:
			raise Exception('REDUNDANT USER INFORMATION!')
		elif len(user_dicts) == 1:
			return user_dicts[0]
		else: # len(user_dicts) == 0
			return False

	def _set_to_db(self):
		user_dict = self._default_dict()
		self.USERS.insert_one(user_dict)

	@property
	def dict(self):
		user_dict = self._get_from_db()
		if user_dict:
			log.debug('ACCOUNT ID IS: '+ str(user_dict['account']['id']))
			# delete the ObjectId('94569463') thing because it is not JSON serializable
			del user_dict['_id']
			return user_dict
		else:
			raise Exception('There was no user in the database.  The user should have been added when it was first __init__ed!')

	@property
	def identifier(self):
		return self.dict['account']

	def _mongo_identifier_dict(self):
		return {
			'account.type': self.account_type,
			'account.id': self.account_id,
		}

	def _default_dict(self):
		return {
			'account': {
				'type': self.account_type,
				'id': self.account_id,
			},
			'learned_node_ids': [],
			'prefs': {
				'display_name_capitalization': None, # can be null, "sentence", or "title"
				'underline_definitions': False, # can be true or false # do you want definitions to be underlined in the DAG view?
				'show_description_on_hover': False, # can be true or false
				'restrict_to_subject': False,
				'enforce_learn_order': True,
				'subject': 'graph theory',
				'goal_node_id': None,
				'requested_pregoal_node_id': None,
				'always_send_absolute_dominion': True,
				'always_send_learnable_pregoals': True,
				'send_learnable_pregoal_number': 1,
				'always_send_goal': False,
				'always_send_unlearned_dependency_tree_of_goal': False,

				'always_accept_suggested_goal': False,
			},
		}

	def learn_node(self, node_id):
		self.USERS.update(self._mongo_identifier_dict(), {'$addToSet': {'learned_node_ids': node_id}}, False)
		# if newly learned node is the current goal, update goal
		if self.dict['prefs']['goal_node_id'] == node_id:
			self.set_pref({'goal_node_id': None})
		# same for requested pregoal
		if self.dict['prefs']['requested_pregoal_node_id'] == node_id:
			self.set_pref({'requested_pregoal_node_id': None})
		# send info down to all other clients (if user is logged in on multiple computers)
		# tornado.websockethandler.send_to_multiple_accounts({ command: 'learn-node', node_id: node_id })

	def unlearn_node(self, node_id):
		self.USERS.update(self._mongo_identifier_dict(), {'$pull': {'learned_node_ids': node_id}}, False)
		# send info down to other clients....

	def set_pref(self, pref_dict):
		one_pref_set = False
		for key, value in pref_dict.items():
			if one_pref_set:
				raise ValueError('Multiple keys existed in pref_dict.  Meant for only one key at a time.')
			# same thing, but replace current pref value in database with pref_dict value
			# for example, pref_dict could be { underline_definitions: true }
			self.USERS.update(self._mongo_identifier_dict(), {'$set': {('prefs.'+key): value}}, False)
			one_pref_set = True

	def set_prefs(self, pref_dict):
		for key, value in pref_dict.items():
			log.debug('setting pref --> key: {}, value: {}'.format(key, value))
			temp_dict = dict()
			temp_dict[key] = value
			self.set_pref(temp_dict)

	def extend(self, other_user): # merges users together (overwriting self), giving other_user priority for any discrepancies.
		# add other_user learned_node_ids to self learned_node_ids:
		self.USERS.update(self._mongo_identifier_dict(), {'$addToSet': {'learned_node_ids': {'$each': other_user.dict['learned_node_ids']}}}, False)
		# add other_user prefs to self prefs:
		self.set_prefs(other_user.dict['prefs'])

	def _unique_local_id(self):
		if self.account_type != 'local':
			log.warn('This function was intended for local accounts.  This error message was created as a safety to make sure you didn\'t make a mistake.  If you are sure you want to use this function, then you can remove this error message from the code entirely.')
		# get all local user ids from db
		local_dicts = list(self.USERS.find({'account.type': 'local'}))
		local_ids = [local_dict['account']['id'] for local_dict in local_dicts]
		proposed_id = 1
		while proposed_id in local_ids: proposed_id += 1
		if proposed_id > 100:
			log.warn('generated unique local id is {}.  This is a high number.  Are local accounts getting deleted properly?'.format(proposed_id))
		return proposed_id

