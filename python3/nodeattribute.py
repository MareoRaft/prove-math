#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

#################################### MAIN #####################################
import subprocess

class NodeAttribute:
	def __init__(self, dic):

	def __repr__(self):
		msg = "(%s, %s)\n" % (self.key, self.value)
		return msg

	@property
	def key(self):
		return self.key

	@name.setter
	def key(self, new_key):
		self.key = new_key

	@property
	def value(self):
		return self.value

	@name.setter
	def value(self, new_value):
		self.value = new_value

	def export_html(self):
		return subprocess.call(['../lib/Markdown.pl', '<<<', '"', self.value, '"'])
		# run mathjax?
