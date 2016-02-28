from lib.mongo import Mongo


class User: # there's really no point in storing users ephemerally, other than to associate a specific user with a specific websocket


	USERS = Mongo("provemath", "users")

	def __init__(self, initial_identifier):
		if initial_identifier['type'] in ['google', 'facebook', 'github', 'linkedin']:
			self.account_type = initial_identifier['type']
			self.account_id = initial_identifier['id']
			self.logged_in = True
		else:
			self.account_type = 'local'
			self.account_id = 'local account, no id set yet'
			self.logged_in = False

	@property
	def dict(self):
		# if user exists, retrieve their dictionary
		user_dicts = list(self.USERS.find(self._mongo_identifier_dict()))
		user_dict = None
		if len(user_dicts) > 1:
			raise Exception('REDUNDANT USER INFORMATION!')
		elif len(user_dicts) == 1:
			user_dict = user_dicts[0]
		else:
			# otherwise, make a new dictionary and store it into the db
			user_dict = self._default_dict()
			self.USERS.insert_one(user_dict)
		del user_dict['_id'] # delete the ObjectId('94569463') thing because it is not JSON serializable
		return user_dict

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
			},
		}

	def learn_node(self, node_id):
		self.USERS.update(self._mongo_identifier_dict(), {'$addToSet': {'learned_node_ids': node_id}}, False)
		# send info down to all other clients (if user is logged in on multiple computers)
		# tornado.websockethandler.send_to_multiple_accounts({ command: 'learn-node', node_id: node_id })

	def unlearn_node(self, node_id):
		self.USERS.update(self._mongo_identifier_dict(), {'$pull': {'learned_node_ids': node_id}}, False)
		# send info down to other clients....

	def set_pref(self, pref_dict):
		one_pref_set = False
		for key in pref_dict:
			if one_pref_set:
				raise ValueError('Multiple keys existed in pref_dict.  Meant for only one key at a time.')
			value = pref_dict[key]
			# same thing, but replace current pref value in database with pref_dict value
			# for example, pref_dict could be { underline_definitions: true }
			self.USERS.update(self._mongo_identifier_dict(), {'$set': {('prefs.'+key): value}}, False)
			one_pref_set = True
