import networkx as nx
import graph_extend
import digraph_extend

def test_validate():
	DG = nx.DiGraph()
	DG.add_edges_from([
		['a', 'b'],
		['c', 'd'],
	])
	# assert DG.validate()

	undirected = nx.convert_to_undirected(DG)
	# assert undirected.validate()


test_validate()
