#!/usr/bin/env python3
import networkx as nx

G = nx.DiGraph() # in particular, our graph will be a DIRECTED ACYCLIC GRAPH (DAG)
# that is, the term DAG by definition means directed adirectedcyclic graph.  cycles are ok.  directed cycles are not.

G.add_edges_from([
	('a', 'c'),
	('b', 'c'),
])
# FG.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)]) # weighted edges!

# addition to the methods Graph.nodes(), Graph.edges(), and Graph.neighbors(), iterator versions (e.g. Graph.edges_iter()) can
H = G.subgraph(['a', 'c'])

print(H.edges())

G.add_edges_from([
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
print(G.neighbors('c')) # this is DIRECTED.  shows the CHILDREN.



# undirected = nx.convert_to_undirected(G)
# print(undirected.connected_components())

print(G.degree())
print(G.degree().values())



print (nx.is_directed_acyclic_graph(G))

print('flow hierarchy')
print(nx.flow_hierarchy(G))

print('ancestors of e: ') # finds ALL ancestors of a node
print(nx.ancestors(G, 'e'))

print('descendants of a: ') # finds ALL descendants of a node
print(nx.descendants(G, 'a'))


# https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.dag.descendants.html


# C = nx.transitive_closure(G) # this would create an edge (a,b) whenever there is a path from a to b.  We can THEN use .ancestors() to find ALL ancestors of a node, not just immediate ancestors.
# lots of good stuff http://networkx.github.io/documentation/development/reference/algorithms.dag.html

# you may need the full path:
# networkx.algorithms.dag.is_directed_acyclic_graph, for example

# print(G.shortest_path('a', 'd'))


# there are some useful stuff like traversal by DFS.  for example:
# https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.traversal.depth_first_search.dfs_predecessors.html?highlight=predecessor#networkx.algorithms.traversal.depth_first_search.dfs_predecessors









# all_neighbors # finds predecessors and successors! (built-in)
# DG.successors(node): # finds all successors of a node in a DiGraph (built-in)
# DG.predecessors(node): # finds all predecessors of a node in a Directed Graph (built-in)

def predecessor(DG, node): # finds any predecessor of a node in a Directed Graph (in the future this should NOT depend on DG.predecessors(node), but instead re-implement the code of .predecessors and stop after finding 1)
	if not nx.is_directed(DG):
		raise Exception('is_source only accepts DiGraphs as input')
	return DG.predecessors(node)[0]

def successor(DG, node): # should follow the same exact pattern as predecessor
	if not nx.is_directed(DG):
		raise Exception('is_source only accepts DiGraphs as input')
	return DG.successors(node)[0]

# common_neighbors # this returns common (parents or children) (built-in) # not too useful :(

# _iter suffix # when _iter is added to the end of many of these functions, you get an iterator

def is_source(DG, node): # checks if a node is a source of a Directed Graph
	if not nx.is_directed(DG):
		raise Exception('is_source only accepts DiGraphs as input')
	return nx.predecessor() == None

def find_source(DAG): # finds any source in Directed A(dir)cyclic Graph
	if not nx.is_directed_acyclic_graph(DAG):
		raise Exception('find_source only accepts Directed A(dir)cyclcic Graphs as input')
	currentNode = DAG.nodes[0]
	while( not DAG.is_source(currentNode) ):
		currentNode = DAG.predecessor(currentNode)
	return currentNode





