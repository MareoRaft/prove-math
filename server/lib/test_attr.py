import pytest

from lib.score import ScoreCard
from lib.attr import *

class Node:
	pass

def test_init():
	node = Node()

	# minimal
	a = Attr(node=node, name='thing', cclass=int)
	assert a.name == 'thing'
	assert a.cclass == int

	# str
	a = Attr(node=node, name='color', value='green', cclass=str)
	assert a.value == 'green'

	# int, with a default
	a = Attr(
		node=node,
		name='importance',
		cclass=int,
		default=-1
	)
	assert a.value == -1

	# maximal
	def examples_setter(attr, new_examples):
		for x in new_examples:
			print("complain")
		return new_examples
	a = Attr(
		node=node,
		name='examples',
		cclass='list of content str',
		setter=examples_setter,
		value=['one', 'two']
	)
	assert a.value == ['one', 'two']

def test_as_dict():
	node = Node()
	a = Attr(node=node, name='thing', cclass=int)
	dic = a.as_dict()
	del dic['score_card']
	assert dic == {
		"name": "thing",
		"value": 0,
	}

