import re
import random
import json
from itertools import chain
from collections import OrderedDict
from copy import deepcopy

from lib import markdown2

def render_content(string):
	""" see main.js for the original version of this function """
	assert isinstance(string, str)
	string = re.sub(r'\\', '\\\\', string) # g (global) is default

	# run markdown server-side
	string = markdown2.markdown(string, extras=["code-friendly", "underline"])
	string = string.strip()

	# enable images
	string = re.sub(r'img(\d+)', '<img src="image/$1.jpg" />', string)
	string = re.sub(r'\\includegraphics\{(.*?)\}', '<img src="image/$1.jpg" />', string)

	return string

def increment_string_counter(string):
	""" example input ==> output:
		word ==> word2
		word0 ==> word1
		word1 ==> word2
		word764 ==> word765
	"""
	match = re.match(r'^(.*?)(\d*)$', string)
	if match is None:
		raise ValueError('input string did not match regex')
	head = match.group(1)
	tail = match.group(2)
	if tail == '':
		tail = '1'
	tail = str(int(tail) + 1)
	new_string = head + tail
	return new_string

def move_attribute(dic, aliases, strict=True):
	for key, value in dic.items():
		if key in aliases:
			del dic[key]
			return value
	if strict:
		raise KeyError('Could not find any of the following keys: {} in the soon-to-be Node {}.'.format(aliases, dic))
	else:
		return None

def find_key(dic, keys):
	for key in dic:
		if key in keys:
			return key
	raise KeyError('Could not find any of the following keys {} in the input dictionary {}'.format(keys, dic))

def string_to_bool(string):
	string = string.lower()
	if string == "true":
		return True
	elif string == "false":
		return False
	else:
		raise ValueError('Cannot convert string to bool.')

def dunderscore_count(string):
	dunderscore_list = re.findall(r'__', string)
	return len(dunderscore_list)

def remove_outer_dunderscores(s):
	# takes in a string like "__hi__", and returns "hi"
	if len(s) >= 4 and s[:2] == "__" and s[-2:] == "__":
		s = s[2:-2]
	return s

def reduce_string(string):
	return re.sub(r'[_\W]', '', string).lower()

def random_string(length):
	word = ''
	for i in range(length):
		word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789')
	return word

def json_import(file_path):
	print("Importing from: " + str(file_path))
	with open(file_path) as file_pointer:
		dictionary = json.load(file_pointer)
		# file_pointer.close() # according to SO ppl, this is called implicitly anyway: http://stackoverflow.com/questions/20199126/reading-a-json-file-using-python
	return dictionary

def json_export(json_list, file_path):
	try:
		print("Saving json to File : "+ str(file_path))
		with open(file_path, 'w') as outfile:
			json.dump(json_list, outfile)
	except TypeError:
		print("List is not in Json format.")
		print("Pass in object as example.__dict__")

def strip_underscores(dictionary):
	dic_copy = deepcopy(dictionary)
	for key, value in dic_copy.items():
		if key[0] == '_':
			del dictionary[key]
			dictionary[key[1:]] = value
	return dictionary

def flatten_list_of_lists(lis):
	new_list = []
	for el in lis:
		if type(el) == list:
			new_list = new_list + el
		else:
			new_list.append(el)
	return new_list

def append_value_to_key(dic, key, value, unpack_key=False):
	"""This is a helper function for reverse_dict."""
	if not unpack_key:
		if not key in dic:
			dic[key] = set()
		dic[key].add(value)
	else:
		for key_el in key:
			append_value_to_key(dic, key_el, value)

def reversed_dict(dic, unpack_values=False):
	""" As it is, always returns a dictionary whose values are SETS.

	If a dictionary is interpreted as a MAP from its KEYS to the ELEMENTS of its values, then the inverse of this map is reverse_dict(dictionary).
	"""
	inv_dict = dict()
	for key, value in dic.items():
		append_value_to_key(inv_dict, value, key, unpack_key=unpack_values) # Notice that key and value are switched on purpose!
	return inv_dict


class DictToObject:


	def __init__(self, dic):
		for key, value in dic.items():
			setattr(self, key, value)
	def __eq__(self, other):
		return self.id == other.id
	def __ne__(self, other):
		return not self.__eq__(other)
	def __hash__(self): # this makes the objects "hashable"!
		return hash(self.__dict__.values())
	def __repr__(self): # this is just for convenience when outputting stuff to the terminal
		return 'DictToObject(' + str(self.__dict__) + ')'

