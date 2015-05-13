import networkx as nx

G = nx.DiGraph()

G.add_edges_from([
	('a', 'c'),
	('b', 'c'),
])
# FG.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)]) # weighted edges!

print(G.neighbors('c')) # this is DIRECTED.  shows the CHILDREN.

# addition to the methods Graph.nodes(), Graph.edges(), and Graph.neighbors(), iterator versions (e.g. Graph.edges_iter()) can

H = G.subgraph(['a', 'c'])

print(H.edges())

G.add_edges_from([
	('c', 'd'),
	('g', 'h'),
	('h', 'i'),
	('w', 'x'),
])

# undirected = nx.convert_to_undirected(G)
# print(undirected.connected_components())

print(G.degree())
print(G.degree().values())



print (nx.is_directed_acyclic_graph(G))

print('flow hierarchy')
print(nx.flow_hierarchy(G))

print('ancestors') # finds the direct ancestors of 'c'
print(nx.ancestors(G, 'c'))

print('descendants') # finds the direct descendants of 'c'
print(nx.descendants(G, 'c'))


C = nx.transitive_closure(G) # this would create an edge (a,b) whenever there is a path from a to b.  We can THEN use .ancestors() to find ALL ancestors of a node, not just immediate ancestors.

# lots of good stuff http://networkx.github.io/documentation/development/reference/algorithms.dag.html
