import json
from itertools import chain

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
	for key, value in dictionary.items():
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

def reverse_dict(dic, unpack_values=False):
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

