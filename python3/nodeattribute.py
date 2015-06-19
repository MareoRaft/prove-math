#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

################################## HELPERS ####################################
#################################### MAIN #####################################
import subprocess
import re


class NodeAttribute:


	def __init__(self, dic):
		if len(dic) != 1:
			raise ValueError('Input dictionary should have length 1')
		for the_key, the_value in dic.items():
			self.key = the_key
			self.value = the_value

	def __repr__(self):
		string = "NodeAttribute({%r: %r})" % (self.key, self.value)
		return string

	def __str__(self):
		return "{%r: %r}" % (self.key, self.value)

	@property
	def key(self):
		return self._key

	@key.setter
	def key(self, new_key):
		if new_key not in {'definition', 'def', 'theorem', 'thm', 'exercise', 'note', 'plural', 'intuition', 'examples', 'counterexamples', 'proofs'}:
			raise ValueError(new_key + ' is not an accepted key.')
		self._key = new_key

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, new_value):
		# run value through some sort of string validator:
		# make sure it is a string!
		if not isinstance(new_value, str):
			TypeError('We only support strings.  But soon we will support videos and images too.')
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
		# if begins with something weird, complain
		if not re.match(r'^[\w\$]', new_value):
			ValueError('String should start with word character or $ sign for LaTeX drop-in.')
		# capitalize first letter
		new_value = new_value.capitalize()
		# if it doesn't end with a period, complain
		if not re.match(r'\.$', new_value):
			ValueError('String should end with a period!')
		# run mathjax on any $dropins$ to make sure they're valid
		# blar node.js mathjax new_value
		# if everything passes, set it
		self._value = new_value

	def as_html(self):
		return subprocess.check_output(['../lib/Markdown.pl', '<<<', '"', self.value, '"'])

		# check out
		# try:
		#     print subprocess.check_output(["ping", "-n", "2", "-w", "2", "1.1.1.1"])
		# except subprocess.CalledProcessError, e:
		#     print "Ping stdout output:\n", e.output
		#
		# http://stackoverflow.com/questions/7575284/check-output-from-calledprocesserror/8235171#8235171
		# http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call


