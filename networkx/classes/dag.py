#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')
###############################################################################

import networkx as nx

def source(DAG): # finds any source in Directed A(dir)cyclic Graph
	if not nx.is_directed_acyclic_graph(DAG):
		raise TypeError('find_source only accepts Directed A(dir)cyclcic Graphs as input')
	currentNode = DAG.nodes[0]
	while( not DAG.is_source(currentNode) ):
		currentNode = DAG.predecessor(currentNode)
	return currentNode

def sources(DAG): # finds the sources in a Directed A(dir)cyclic Graph
	if not nx.is_directed_acyclic_graph(DAG):
		raise TypeError('sources only accepts Directed A(dir)cyclcic Graphs as input')
	dag = DAG.copy()
	sources = []
	while(dag.nonempty()):
		source = source(dag)
		sources.push(source)
		sourceAndDescendants = {source} | set(source.descendants)
		dag = dag.subgraph( set(dag.nodes) - sourceAndDescendants )
	return sources

def common_descendant_sources(DAG, nbunchA, nbunchB):
	if not nx.is_directed_acyclic_graph(DAG):
		raise TypeError('this func is for Directed A(dir)cyclic Graphs only') # we need a builtin type handling!
	return sources( DAG.subgraph(common_descendants(DAG, nbunchA, nbunchB)) )


