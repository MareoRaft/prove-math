from lib.mongo import Mongo


class User: # there's really no point in storing users ephemerally, other than to associate a specific user with a specific websocket


	USERS = Mongo("provemath", "users")

	def __init__(self, initial_identifier):
		if initial_identifier['account_type'] in ['google', 'facebook', 'github', 'linkedin']:
			self.account_type = initial_identifier['account_type']
			self.account_id = initial_identifier['account_id']
		else:
			raise ValueError('Account type not supported.')

	@property
	def dict(self):
		# if user exists, retrieve their dictionary
		user_dicts = list(self.USERS.find(self._identifier_dict()))
		if len(user_dicts) > 1:
			raise Exception('REDUNDANT USER INFORMATION!')
		elif len(user_dicts) == 1:
			user_dict = user_dicts[0]
			user_dict['_id'] = str(user_dict['_id'])
			return user_dict
		else:
			# otherwise, make a new dictionary and store it into the db
			temp_dict = self._default_dict()
			self.USERS.insert_one(temp_dict)
			return temp_dict

	def _identifier_dict(self):
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
				'display_name_capitalization': "title", # can be null, "sentence", or "title"
				'underline_definitions': False, # can be true or false # do you want definitions to be underlined in the DAG view?
				'show_description_on_hover': False, # can be true or false
			},
		}

	def learn_node(self, node_id):
		self.USERS.update(self._identifier_dict(), {'$addToSet': {'learned_node_ids': node_id}}, False)
		# send info down to all other clients (if user is logged in on multiple computers)
		# tornado.websockethandler.send_to_multiple_accounts({ command: 'learn-node', node_id: node_id })

	def unlearn_node(self, node_id):
		self.USERS.update(self._identifier_dict(), {'$pull': {'learned_node_ids': node_id}}, False)
		# send info down to other clients....

	def set_pref(self, pref_dict):
		one_pref_set = False
		for key in pref_dict:
			if one_pref_set:
				raise ValueError('Multiple keys existed in pref_dict.  Meant for only one key at a time.')
			value = pref_dict[key]
			# same thing, but replace current pref value in database with pref_dict value
			# for example, pref_dict could be { underline_definitions: true }
			self.USERS.update(self._identifier_dict(), {'$set': {('prefs.'+key): value}}, False)
			one_pref_set = True
