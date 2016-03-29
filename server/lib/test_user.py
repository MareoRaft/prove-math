import pytest
from lib import user
from lib.user import User

def test___init__():
	# get existing user
	sue = User({'type': 'facebook', 'id': 'S0U0E0' })
	assert sue.dict['account']['type'] == 'facebook'

	# create a new user
	mo = User({'type': 'google', 'id': 'xPr' })
	assert mo.dict['account']['id'] == 'xPr'

def test_learn_node():
	mo = User({'type': 'google', 'id': 'xPr' })
	mo.learn_node('nonemptygraph')
	assert 'nonemptygraph' in mo.dict['learned_node_ids']
	mo_fresh = User({'type': 'google', 'id': 'xPr' })
	assert 'nonemptygraph' in mo_fresh.dict['learned_node_ids']

	matt_thick = User({'type': 'github', 'id': 'ggg' })
	assert 'nonemptygraph' not in matt_thick.dict['learned_node_ids']

def test_unlearn_node():
	mo = User({'type': 'google', 'id': 'xPr' })
	mo.learn_node('vertex')
	assert 'vertex' in mo.dict['learned_node_ids']
	mo.unlearn_node('vertex')
	assert 'vertex' not in mo.dict['learned_node_ids']

def test_set_pref():
	matt = User({'type': 'github', 'id': 'ggg' })
	matt.set_pref({ 'anything': 'now' })
	assert matt.dict['prefs']['anything'] == 'now'
	matt.set_pref({ 'anything': 'notnow' })
	assert matt.dict['prefs']['anything'] == 'notnow'

	with pytest.raises(ValueError):
		matt.set_pref({ 'one': 'more', 'thing': 'here' })

def test_set_prefs():
	matt = User({'type': 'github', 'id': 'hhsetprefshh' })
	matt.set_prefs({
		'one': 'a',
		'two': 'b',
	})
	print(str(matt.dict))
	assert matt.dict['prefs']['one'] == 'a'
	assert matt.dict['prefs']['two'] == 'b'

def test_extend():
	matt = User({'type': 'facebook', 'id': 'hhextendhh' })
	matt.learn_node('node-one')
	john = User({'type': 'linkedin', 'id': 'hhextendhh' })
	john.learn_node('node-two')
	matt.extend(john)
	assert matt.dict['learned_node_ids'] == ['node-one', 'node-two']

