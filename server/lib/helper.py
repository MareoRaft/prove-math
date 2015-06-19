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
