import pytest

from lib.attr import *

def test_init():
	# minimal
	a = Attr('thing', ttype=int)
	assert a.name == 'thing'
	assert a.ttype == int

	# str
	a = Attr(name='color', value='green', ttype=str)
	assert a.value == 'green'

	# int, with a default
	a = Attr(
		name='importance',
		ttype=int,
		default=-1
	)
	assert a.value == -1

	# maximal
	def examples_setter(new_examples):
		for x in new_examples:
			print("complain")
		return new_examples
	a = Attr(
		name='examples',
		ttype='list of content str',
		setter=examples_setter,
		value=['one', 'two']
	)
	assert a.value == ['one', 'two']


