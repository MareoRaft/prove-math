import networkx as nx
import dag

def test_validate():
	DAG = nx.DAG()
	DAG.add_edges_from([
		['a', 'b'],
		['b', 'c'],
		['c', 'd'],
	])
	assert DAG.validate()

	DAG.add_edge('d', 'a')
	try:
		DAG.validate() # this crashes the program unless the specific error is listed below.
		assert False # this line always fails.  The point is that we don't want this line to ever run.  If it does, something went wrong!
	except TypeError as e:
		assert str(e) == 'Not a Directed A(dir)cyclcic Graph!'

# def test_source():
# 	DAG = DAG()
# 	DAG.add_edges_from([
# 		['a', 'b'],
# 		['b', 'c'],
# 		['c', 'd'],
# 	])
# 	assert DAG.source() == 'a'

# def test_sources():
# 	DAG = DAG()
# 	DAG.add_edges_from([
# 		['a', 'b'],
# 		['b', 'c'],
# 		['c', 'd'],
# 	])
# 	assert DAG.sources() == ['a']

# 	DAG.add_edge('z', 'd')
# 	assert set(DAG.sources()) == {'a', 'z'}

