""" The goal of this file is to run methods on really big graphs.  elapsed_times.log will automatically record the results, without any logging explicitly stated in this file.
"""
import pytest

from lib.pmdag import *
from lib.mongo import Mongo
from lib.math_graph import MathGraph
from lib.node import create_appropriate_node

def update_our_MG():
	# 1. grab nodes and edges from database
	all_node_dicts = list(Mongo("provemath", "nodes").find())
	# print('number of node dicts is: {}'.format(len(all_node_dicts)))

	# 2. create a networkx graph with the info...
	global our_MG
	our_MG = MathGraph()
	for node_dict in all_node_dicts:
		# try:
		node = create_appropriate_node(node_dict)
		# except Exception as e:
			# print('\nerror.  could not create_appropriate_node.  node_dict was: '+str(strip_underscores(node_dict)))
		our_MG.add_n(node)
	for node_id in our_MG.nodes():
		node = our_MG.n(node_id)
		for dependency_id in node.dependency_ids:
			our_MG.add_edge(dependency_id, node_id)
	our_MG.validate() # make sure it's still Acyclic
	our_MG.remove_redundant_edges()
	print('Node array loaded with length: {}'.format(len(our_MG.nodes())))
	print('Edge array loaded with length: {}'.format(len(our_MG.edges())))

def test_unselected_dependency_tree():
	our_mongo = Mongo("provemath", "nodes")
	update_our_MG()

	G = our_MG
	G.unselected_dependency_tree('artin', ['fixer', 'algebaric', 'orderhomslf', 'fielddegree', 'charofr', 'minpolyrootminpoly', ])
