import re
import subprocess

from lib.helper import json_import
from lib.node import create_appropriate_node, find_node_from_id
from lib.mongo import Mongo

file_name = input('What is the name of the pre-json file?: ')
re.sub(r'^data/', '', file_name)
re.sub(r'\.pre-json$', '', file_name)
file_path = 'data/' + file_name + '.pre-json'
subprocess.check_output(['lib/pre-json_to_json.pl', file_path])

new_data_dictionary = json_import('data/' + file_name + '.json')


collection = input('Which collection should we store the nodes in? (nodes): ')
if collection == '':
	collection = 'nodes'
db_nodes = Mongo("provemath", collection)
collection = input('Which collection should we store the edges in? (edges): ')
if collection == '':
	collection = 'edges'
db_edges = Mongo("provemath", collection)

nodes = []
for pre_node in new_data_dictionary['nodes']:
	node = create_appropriate_node(pre_node)
	try:
		db_nodes.insert_one(node.__dict__)
		nodes.append(node)
		for i in range(len(node.dependencies)):
			# this is not because we need to find the node that is the dependency.  This is merely to make sure the dependency exists!  This is just error checking!
			dependency_node = find_node_from_id(nodes, node.dependency_ids[i])
			db_edges.insert_one({
				"source": node.dependency_ids[i],
				"target": node.id,
				"_id": 'SOURCE:' + node.dependency_ids[i] + ',' + 'TARGET:' + node.id,
				"source_name": node.dependencies[i],
				"target_name": node.name,
			})
	except:
		print('skipping (perhaps partially) node: '+node.id)

print('Transfer complete!!!!')
