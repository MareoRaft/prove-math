#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

#################################### MAIN #####################################
import subprocess

class NodeAttribute:
	def __init__(self, dic):
		if len(dic) != 1:
			raise ValueError('Input dictionary should have length 1')
		for the_key, the_value in dic.items():
			self.key = the_key
			self.value = the_value

	def __repr__(self):
		string = "(%s, %s)" % (self.key, self.value)
		return string

	@property
	def key(self):
		return self.__key

	@key.setter
	def key(self, new_key):
		if new_key not in {'definition', 'def', 'theorem', 'thm', 'exercise', 'note', 'plural', 'intuition', 'examples', 'counterexamples', 'proofs'}:
			raise ValueError(new_key + ' is not an accepted key.')
		self.__key = new_key

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, new_value):
		# run value through some sort of string validator:
		# make sure its UTF-8
		try:
		    new_value.encode() # look at: http://stackoverflow.com/questions/12053107/test-a-string-if-its-unicode-which-utf-standard-is-and-get-its-length-in-bytes
		    print("string is UTF-8, length %d bytes" % len(new_value))
		except UnicodeError:
		    print("string is not UTF-8")
		# not too short, not too long
		if len(new_value) < 5:
			raise ValueError('The value string is too short.  Make sure you are inputting complete information!')
		if len(new_value) > 600:
			raise ValueError('The value string is too long.  It\'s too wordy or complicated!')
		# reasonable sentence things:
		# if begins with letter, capitalize.
		# if it doesn't end with a period, complain
		# run mathjax on any $dropins$ to make sure they're valid
		# blar node.js mathjax new_value
		# if everything passes, set it
		self.__value = new_value

	def export_html(self):
		return subprocess.call(['../lib/Markdown.pl', '<<<', '"', self.value, '"'])

