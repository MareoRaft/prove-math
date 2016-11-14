########################## IMPORTS ##########################
import pytest
import networkx as nx

from statement_implication_contractor import *
from lib.node import create_appropriate_node


########################## HELPERS ##########################

########################### MAIN ###########################
def test_remove_sources_repeatedly():
	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	remove_sources_repeatedly(DG)
	assert not DG.nodes()

	DG = nx.DiGraph()
	DG.add_path(['a', 'b', 'c'])
	DG.add_path(['a', 'd', 'c'])
	remove_sources_repeatedly(DG)
	assert not DG.nodes()

	DG = nx.DiGraph()
	DG.add_cycle(['a', 'b', 'c'])
	remove_sources_repeatedly(DG)
	assert len(DG.nodes()) == 3

	DG = nx.DiGraph()
	DG.add_edge('s', 'a')
	DG.add_cycle(['a', 'b', 'c', 'd'])
	DG.add_edge('d', 't')
	remove_sources_repeatedly(DG)
	assert DG.sources() == set()
	assert len(DG.nodes()) == 5








