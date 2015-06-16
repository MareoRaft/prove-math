#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

#################################### MAIN #####################################
from nodeattribute import NodeAttribute

def test___init__():
	try:
		you = NodeAttribute({'hi': 'there', 'are': 'we'})
		assert False
	except ValueError as e:
		assert str(e) == 'Input dictionary should have length 1'

	me = NodeAttribute({'definition': '123123'})
	assert me.key == 'definition'
	assert me.value == '123123'
	assert me.__repr__() == '(definition, 123123)'

def test_export_html():
	me = NodeAttribute({'thm': 'this is sparta'})
	assert me.export_html() ==  'this is sparta'

	me = NodeAttribute({'thm': '**bold**, __underline__, and *italics* and _italics_'})
	assert me.export_html() ==  '<b>bold</b>, <u>underline</u>, and <i>italics</i> and <i>italics</i>'

