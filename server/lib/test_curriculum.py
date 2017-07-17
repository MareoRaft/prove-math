import pytest

from lib.curriculum import *
from lib.pmdag import PMDAG

def test_unique_string():
	# simple
	strings = ['one', 'two', 'three']
	assert unique_string(strings) == 'a'

	# avoid a value
	strings = ['a', 'one', 'two', 'three']
	assert unique_string(strings) not in strings

def test_init():
	# empty list should fail
	G = PMDAG()
	with pytest.raises(ValueError):
		Curriculum(G, node_ids=[])

	# one element list
	# VERTEX and ONEDGESONVERTICES must be in the nodes collection of the provemath database on your local mongo for this to work!
	G = PMDAG()
	G.add_node('vertex')
	ids = ['vertex']
	c = Curriculum(G, node_ids=ids) # this errors if vertex is not in the DB, which it should.
	assert c.node_ids == ['vertex']

	# multiple element list
	G = PMDAG()
	G.add_nodes_from(['vertex', 'onedgesonvertices'])
	ids = ['vertex', 'onedgesonvertices']
	c = Curriculum(G, node_ids=ids)
	assert c.node_ids == ['vertex', 'onedgesonvertices']

	# a nonexistent id should fail
	with pytest.raises(StopIteration):
		Curriculum(G, node_ids=[''])
	with pytest.raises(StopIteration):
		Curriculum(G, node_ids=['nonexistantnodeid'])

	# make sure curriculum gets an id itself
	ids = ['vertex']
	c = Curriculum(G, node_ids=ids)
	assert type(c.id) == str

	# make sure name gets set
	ids = ['vertex']
	c = Curriculum(G, node_ids=ids, name='Combinatorics')
	assert c.name == 'Combinatorics'

	# make sure bad names don't get set
	with pytest.raises(TypeError):
		Curriculum(G, node_ids=ids, name=['i\'m', 'a', 'list'])

def test_as_dict():
	# simple dict
	G = PMDAG()
	G.add_node('vertex')
	ids = ['vertex']
	c = Curriculum(G, node_ids=ids)
	assert c.as_dict() == {
		'_id': c.id,
		'_node_ids': ['vertex'],
		'_name': None
	}

	# complex dict
	G = PMDAG()
	G.add_nodes_from(['vertex', 'onedgesonvertices'])
	ids = ['vertex', 'onedgesonvertices']
	c = Curriculum(G, node_ids=ids, name='Graph Theory')
	assert c.as_dict() == {
		'_id': c.id,
		'_node_ids': ['vertex', 'onedgesonvertices'],
		'_name': 'Graph Theory',
	}

CURRICULUMS = Mongo('provemath', 'curriculums')

def test_store():
	G = PMDAG()
	G.add_node('vertex')
	ids = ['vertex']
	c = Curriculum(G, node_ids=ids)
	c.store()
	found_cs = list(CURRICULUMS.find({'_id': c.id}))
	assert len(found_cs) == 1
	found_c = found_cs[0]
	assert c.as_dict() == found_c
	# DELETE the guy you just made, so as not to clutter the DB
	CURRICULUMS.delete_one({'_id': c.id})

