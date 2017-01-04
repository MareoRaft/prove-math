import re
import subprocess

from lib.helper import json_import, strip_underscores
from lib.node import create_appropriate_node
from lib.mongo import Mongo
from lib.math_graph import MathGraph

file_name = input('What is the name of the pre-json file?: ')
file_name = re.sub(r'^data/', '', file_name)
file_name = re.sub(r'\.pre-json$', '', file_name)
file_path = 'data/' + file_name + '.pre-json'
subprocess.run(['lib/pre-json_to_json.pl', file_path], check=True)

json_file_path = 'data/' + file_name + '.json'
new_data_dictionary = json_import(json_file_path)
# delete .json file
# subprocess.check_output(['rm', json_file_path])

collection = input('Which collection should we store the nodes in? (nodes): ')
if collection == '':
	collection = 'nodes'
db_nodes = Mongo("provemath", collection)

# actually, i think upsert IS force.
# force = input('Do you want to overwrite any existing nodes?  WARNING: this can result in data loss: ')
# if force.lower() in ['yes', 'ye', 'y']:
# 	force = True
# else:
# 	force = False

# create a graph for information purposes
# 1. grab nodes and edges from database
all_node_dicts = list(db_nodes.find())

# 2. create a networkx graph with the info...
global our_MG
our_MG = MathGraph()
for node_dict in all_node_dicts:
	# try:
	node = create_appropriate_node(strip_underscores(node_dict))
	# except Exception as e:
		# print('\nerror.  could not create_appropriate_node.  node_dict was: '+str(strip_underscores(node_dict)))
	our_MG.add_n(node)
for node_id in our_MG.nodes():
	node = our_MG.n(node_id)
	for dependency_id in node.dependency_ids:
		our_MG.add_edge(dependency_id, node_id)
our_MG.validate() # make sure it's still Acyclic
print('Node array loaded with length: ' + str(len(our_MG.nodes())))
print('Edge array loaded with length: ' + str(len(our_MG.edges())))



# populate new nodes into DB
for pre_node in new_data_dictionary['nodes']:
	node = create_appropriate_node(pre_node)
	try:
		db_nodes.insert_one(node.as_dict())
	except:
		# a blank version of this node already existed, so we need to
		# upsert it in DB
		# if force:
		# 	db_nodes.delete_one({"_id": node.id})
		db_nodes.upsert({"_id": node.id}, node.as_dict())
		# db_nodes.upsert(node.as_dict())
		# then remove it from nodes too and replace with node
		# del nodes[node.id] # errors if no exist
		our_MG.remove_n(node)
	our_MG.add_n(node)

	for i in range(len(node.attrs['dependencies'].value)):
		if node.dependency_ids[i] in our_MG.nodes():
			# this is not because we need to find the node that is the dependency.  This is merely to make sure the dependency exists!  This is just error checking!
			pass
		else:
			# dependency doesn't exist or won't until later on in loop.  so create blank node, add to nodes and db:
			dependency_node = create_appropriate_node({
				"name": node.attrs['dependencies'].value[i],
				"type": "axiom",
			})
			our_MG.add_n(dependency_node)
			db_nodes.insert_one(dependency_node.as_dict())


print('Transfer complete!!!!')
