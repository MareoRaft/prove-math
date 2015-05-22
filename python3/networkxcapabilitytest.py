#!/usr/bin/env python3
import networkx as nx



DG = nx.DiGraph() # in particular, our graph will be a DIRECTED ACYCLIC GRAPH (DAG)
# that is, the term DAG by definition means directed adirectedcyclic graph.  cycles are ok.  directed cycles are not.

DG.add_edges_from([
	('a', 'c'),
	('b', 'c'),
])
# FG.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)]) # weighted edges!

# addition to the methods Graph.nodes(), Graph.edges(), and Graph.neighbors(), iterator versions (e.g. Graph.edges_iter()) can
# DH = DG.subgraph(['a', 'c'])
# print(DH.edges())

DG.add_edges_from([
	('c', 'd'), ('c', 'd2'), ('d', 'e'),
	('g', 'h'),
	('h', 'i'),
	('w', 'x'),
])

# a --> c --> d
# b -->

# g --> h --> i

# w --> x

print('the neighbors (children) of c are: ')
print(DG.neighbors('c')) # this is DIRECTED.  shows the CHILDREN.



# undirected = nx.convert_to_undirected(DG)
# print(undirected.connected_components())

print(DG.degree())
print(DG.degree().values())



print (nx.is_directed_acyclic_graph(DG))

print('flow hierarchy')
print(nx.flow_hierarchy(DG))

print('ancestors of e: ') # finds ALL ancestors of a node
print(nx.ancestors(DG, 'e'))

print('descendants of a: ') # finds ALL descendants of a node
print(nx.descendants(DG, 'a'))


# https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.dag.descendants.html


# C = nx.transitive_closure(G) # this would create an edge (a,b) whenever there is a path from a to b.  We can THEN use .ancestors() to find ALL ancestors of a node, not just immediate ancestors.
# lots of good stuff http://networkx.github.io/documentation/development/reference/algorithms.dag.html

# you may need the full path:
# networkx.algorithms.dag.is_directed_acyclic_graph, for example







# there are some useful stuff like traversal by DFS.  for example:
# https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.traversal.depth_first_search.dfs_predecessors.html?highlight=predecessor#networkx.algorithms.traversal.depth_first_search.dfs_predecessors









# all_neighbors # finds predecessors and successors! (built-in)
# DG.successors(node): # finds all successors of a node in a DiGraph (built-in)
# DG.predecessors(node): # finds all predecessors of a node in a Directed Graph (built-in)

def predecessor(DG, node): # finds any predecessor of a node in a Directed Graph (in the future this should NOT depend on DG.predecessors(node), but instead re-implement the code of .predecessors and stop after finding 1)
	if not nx.is_directed(DG):
		raise TypeError('is_source only accepts DiGraphs as input') # Exceptions are general. Exception >= StandardError >= TypeError
	return DG.predecessors(node)[0]

def successor(DG, node): # should follow the same exact pattern as predecessor
	if not nx.is_directed(DG):
		raise TypeError('is_source only accepts DiGraphs as input')
	return DG.successors(node)[0]

# common_neighbors # this returns common (parents or children) (built-in) # not too useful :(

# _iter suffix # when _iter is added to the end of many of these functions, you get an iterator

def is_source(DG, node): # checks if a node is a source of a Directed Graph
	if not nx.is_directed(DG):
		raise TypeError('is_source only accepts DiGraphs as input')
	return nx.predecessor() == None

def source(DAG): # finds any source in Directed A(dir)cyclic Graph
	if not nx.is_directed_acyclic_graph(DAG):
		raise TypeError('find_source only accepts Directed A(dir)cyclcic Graphs as input')
	currentNode = DAG.nodes[0]
	while( not DAG.is_source(currentNode) ):
		currentNode = DAG.predecessor(currentNode)
	return currentNode

# on hold
# def sources(DAG): # finds the sources in a Directed A(dir)cyclic Graph
# 	if not nx.is_directed_acyclic_graph(DAG):
# 		raise TypeError('sources only accepts Directed A(dir)cyclcic Graphs as input')
# 	currentNode = DAG.nodes[0]
# 	while( not DAG.is_source(currentNode) ):
# 		currentNode = DAG.predecessor(currentNode)
# 	return currentNode




############################################################
print('the in edges of c and d are: ')
print(DG.in_edges(nbunch={'c', 'd'})) # this INCLUDES edges between c and d  :(

print('the out edges of c and d are: ')
print(DG.out_edges(nbunch={'c', 'd'})) # this INCLUDES edges between c and d  :(

print('the in degree of c is: ')
print(DG.in_degree('c'))

print('the in degrees of c and d are: ')
print(DG.in_degree(nbunch={'c', 'd'}))


# there is also a DiGraph.has_successor('a', 'b') if you only want to see if a directed path from 'a' to 'b' exists.
print('the shortest path from a to d is: ')
print(nx.shortest_path(DG, source='a', target='d')) # this finds shortest DIRECTED path


def shortest_anydirectional_path(DG, source=None, target=None):
	if not nx.is_directed(DG):
		raise TypeError('shortest_anydirectional_path is for DiGraphs only')
	G = DG.to_undirected()
	return nx.shortest_path(G, source=source, target=target)

print('the shortest anydirectional path between a and d is: ')
print(shortest_anydirectional_path(DG, source='d', target='a'))


def common_descendants(DG, nbunchA, nbunchB):
	if not nx.is_directed(DG):
		raise TypeError('common_descendants is for DiGraphs only')
	descA = nx.descendants(DG, nbunchA)
	descB = nx.descendants(DG, nbunchB)
	return list(set.intersection(set(descA), set(descB)))


print('the common descendants of a and c are: ')
print(common_descendants(DG, 'a', 'c'))

def common_descendant_sources(DAG, nbunchA, nbunchB):
	if not nx.is_directed_acyclic_graph(DAG):
		raise TypeError('this func is for Directed A(dir)cyclic Graphs only') # we need a builtin type handling!
	return sources( common_descendants(DAG, nbunchA, nbunchB) )







