import re
import subprocess

from lib.helper import json_import
from lib.node import create_appropriate_node
from lib.mongo import Mongo

file_name = input('What is the name of the pre-json file?: ')
file_name = re.sub(r'^data/', '', file_name)
file_name = re.sub(r'\.pre-json$', '', file_name)
file_path = 'data/' + file_name + '.pre-json'
subprocess.check_output(['lib/pre-json_to_json.pl', file_path])

json_file_path = 'data/' + file_name + '.json'
new_data_dictionary = json_import(json_file_path)
# delete .json file
subprocess.check_output(['rm', json_file_path])

collection = input('Which collection should we store the nodes in? (nodes): ')
if collection == '':
	collection = 'nodes'
db_nodes = Mongo("provemath", collection)

nodes = dict() # this is just to keep track of what we do and do not add to the DB.  A smarter way would be to do away with this completely and check mongo directly.
for pre_node in new_data_dictionary['nodes']:
	node = create_appropriate_node(pre_node)
	try:
		db_nodes.insert_one(node.__dict__)
	except:
		# a blank version of this node already existed, so we need to
		# upsert it in DB
		db_nodes.upsert({"_id": node.id}, node.__dict__)
		# then remove it from nodes too and replace with node
		del nodes[node.id] # errors if no exist
	nodes[node.id] = node

	for i in range(len(node.dependencies)):
		if node.dependency_ids[i] in nodes:
			# this is not because we need to find the node that is the dependency.  This is merely to make sure the dependency exists!  This is just error checking!
			pass
		else:
			# dependency doesn't exist or won't until later on in loop.  so create blank node, add to nodes and db:
			dependency_node = create_appropriate_node({
				"name": node.dependencies[i],
				"type": "axiom",
			})
			nodes[dependency_node.id] = dependency_node
			db_nodes.insert_one(dependency_node.__dict__)


print('Transfer complete!!!!')
