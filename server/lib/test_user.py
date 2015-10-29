import pytest
from lib import user
from lib.user import User

def test___init__():
	# get existing user
	sue = User({'account_type': 'facebook', 'account_id': 'S0U0E0' })
	assert sue.dict['account']['type'] == 'facebook'

	# create a new user
	mo = User({'account_type': 'google', 'account_id': 'xPr' })
	assert mo.dict['account']['id'] == 'xPr'

def test_learn_node():
	mo = User({'account_type': 'google', 'account_id': 'xPr' })
	mo.learn_node('nonemptygraph')
	assert 'nonemptygraph' in mo.dict['learned_node_ids']
	mo_fresh = User({'account_type': 'google', 'account_id': 'xPr' })
	assert 'nonemptygraph' in mo_fresh.dict['learned_node_ids']

	matt_thick = User({'account_type': 'github', 'account_id': 'ggg' })
	assert 'nonemptygraph' not in matt_thick.dict['learned_node_ids']

def test_unlearn_node():
	mo = User({'account_type': 'google', 'account_id': 'xPr' })
	mo.learn_node('vertex')
	assert 'vertex' in mo.dict['learned_node_ids']
	mo.unlearn_node('vertex')
	assert 'vertex' not in mo.dict['learned_node_ids']

def test_set_pref():
	matt = User({'account_type': 'github', 'account_id': 'ggg' })
	matt.set_pref({ 'anything': 'now' })
	assert matt.dict['prefs']['anything'] == 'now'
	matt.set_pref({ 'anything': 'notnow' })
	assert matt.dict['prefs']['anything'] == 'notnow'

	try:
		matt.set_pref({ 'one': 'more', 'thing': 'here' })
		assert False
	except ValueError:
		assert True

