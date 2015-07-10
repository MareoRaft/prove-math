#!/usr/bin/env python3
################################## IMPORTS ####################################
import sys

from lib.nodeattribute import NodeAttribute

import subprocess

################################## HELPERS ####################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

#################################### MAIN #####################################
def test___init__():
	try:
		you = NodeAttribute({'hi': 'there', 'are': 'we'})
		assert False
	except ValueError as e:
		assert str(e) == 'Input dictionary should have length 1'

	me = NodeAttribute({'definition': '123123'})
	assert me.key == 'definition'
	assert me.value == '123123'

def test___repr__():
	x = NodeAttribute({'def': 'the fundamental unit of everything'})
	assert x.__repr__() == "NodeAttribute({'def': 'The fundamental unit of everything'})" # the thing i typed to make x in the first place
	y = NodeAttribute({'def': 'the fundamental unit of everything'})
	assert x != y

def test___str__():
	x = NodeAttribute({'exercise': 'This is a complete exercise.'})
	assert str(x) == "{'exercise': 'This is a complete exercise.'}"

def test_as_html():
	me = NodeAttribute({'thm': 'this is sparta'})
	print(subprocess.check_output(['pwd']))
	assert me.as_html() ==  'This is sparta'

	me = NodeAttribute({'thm': '**bold**, __underline__, and *italics* and _italics_'})
	assert me.as_html() ==  '<b>bold</b>, <u>underline</u>, and <i>italics</i> and <i>italics</i>'

