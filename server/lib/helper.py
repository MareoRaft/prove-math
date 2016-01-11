import json

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

