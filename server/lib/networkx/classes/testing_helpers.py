import networkx as nx

#from lib.networkx.classes import digraph_extend
from lib.node import create_appropriate_node, Node

def fill_sample_custom_nodes():
	#creates a graph with a handful of our custom node objects, but no edges
	pre_a = {"type":"theorem","description":"This is node aaaaaaaaaa","name":"A","importance":3}
	a = create_appropriate_node(pre_a)
	pre_b = {"type":"theorem","description":"This is node bbbbbbbbbb","name":"B","importance":4}
	b = create_appropriate_node(pre_b)
	pre_c = {"type":"theorem","description":"This is node cccccccccc","name":"C","importance":4}
	c = create_appropriate_node(pre_c)
	pre_d = {"type":"theorem","description":"This is node dddddddddd","name":"D","importance":6}
	d = create_appropriate_node(pre_d)
	pre_e = {"type":"theorem","description":"This is node eeeeeeeeee","name":"E","importance":8}
	e = create_appropriate_node(pre_e)
	DG = nx.DiGraph()
	DG.add_n(a)
	DG.add_n(b)
	DG.add_n(c)
	DG.add_n(d)
	DG.add_n(e)
	return DG

