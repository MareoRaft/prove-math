import pytest

from lib.curriculum import *

def test_unique_string():
	# simple
	strings = ["one", "two", "three"]
	assert unique_string(strings) == "a"

	# avoid a value
	strings = ["a", "one", "two", "three"]
	assert unique_string(strings) not in strings

def test_init():
	# empty list should fail
	with pytest.raises(ValueError):
		Curriculum([])

	# one element list
	# VERTEX and ONEDGESONVERTICES must be in the nodes collection of the provemath database on your local mongo for this to work!
	ids = ["vertex"]
	c = Curriculum(ids)
	assert c.ids == ["vertex"]

	# multiple element list
	ids = ["vertex", "onedgesonvertices"]
	c = Curriculum(ids)
	assert c.ids == ["vertex", "onedgesonvertices"]

	# a nonexistent id should fail
	with pytest.raises(StopIteration):
		Curriculum([""])
	with pytest.raises(StopIteration):
		Curriculum(["nonexistantnodeid"])

	# make sure curriculum gets an id itself
	ids = ["vertex"]
	c = Curriculum(ids)
	assert type(c.id) == str

	# make sure name gets set
	ids = ["vertex"]
	c = Curriculum(ids, "Combinatorics")
	assert c.name == "Combinatorics"

	# make sure bad names don't get set
	with pytest.raises(ValueError):
		Curriculum(ids, ["i'm", "a", "list"])

def test_as_dict():
	# simple dict
	ids = ["vertex"]
	c = Curriculum(ids)
	assert c.as_dict() == {
		"_id": c.id,
		"_ids": ["vertex"],
		"_name": None
	}

	# complex dict
	ids = ["vertex", "onedgesonvertices"]
	c = Curriculum(ids, "Graph Theory")
	assert c.as_dict() == {
		"_id": c.id,
		"_ids": ["vertex", "onedgesonvertices"],
		"_name": "Graph Theory",
	}

CURRICULUMS = Mongo("provemath", "curriculums")

def test_store():
	ids = ["vertex"]
	c = Curriculum(ids)
	c.store()
	found_cs = list(CURRICULUMS.find({"_id": c.id}))
	assert len(found_cs) == 1
	found_c = found_cs[0]
	assert c.as_dict() == found_c
	# DELETE the guy you just made, so as not to clutter the DB
	CURRICULUMS.delete_one({"_id": c.id})

