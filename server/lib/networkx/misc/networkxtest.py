import networkx as nx


G = nx.DiGraph()

# any hashable Python object can be a node. (not just integers)
G.add_node(1)
G.add_nodes_from([6, 8])
G.add_nodes_from(range(100, 110))

# delete a node
del G.node[100]
# delete a dic attribute
# del G.node[8]['smart'] # causes error if attr doesn't exist in first place

# add edges
G.add_edge(1, 2) # 2 automatically added here
G.add_edges_from([(6, 7), (7, 6)])

# view a node
print(G.node[1])
# view nodes
G.nodes() # see all nodes
G.nodes(data=True) # see all nodes and builtin dictionaries
# view edges
print(G.edges())

# check if node in graph
1 in G

# iterate through nodes
[n for n in G]

# number of nodes
len(G)

# everything works! yay!
# traverse all edges and MORE MORE MORE
# https://networkx.github.io/documentation/latest/reference/classes.digraph.html#overview
