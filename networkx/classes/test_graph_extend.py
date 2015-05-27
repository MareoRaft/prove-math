# this will test the new graph, digraph, and dag methods.
# we want to add a GIT HOOK to automatically run this test before pushing to GitHub

# some testing advice is here: http://docs.python-guide.org/en/latest/writing/tests/
# in particular, "The first step when you are debugging your code is to write a new test pinpointing the bug. While it is not always possible to do, those bug catching tests are among the most valuable pieces of code in your project."

# import unittest
# from unittest import TestCase

# import networkx as nx
# # extend Graph and DiGraph with our files, and create class DAG

# class MyFirstTest (TestCase):
# 	def is_nonnull(self):
# 		nonnull = nx.Graph()
# 		nonnull.add_node('a')
# 		self.assertTrue(nonnull.is_nonnull())

# 		nonnull = nx.Graph()
# 		nonnull.add_edge('s', 't')
# 		self.assertTrue(nonnull.is_nonnull())

# 		nonnull = nx.Graph()
# 		self.assertFalse(nonnull.is_nonnull())

# looking further on the above URL, it seems that pytest is the same but simpler nicer syntax!

# also, there is mock which sounds like a standard Python3 thing.

# I really like the simplicity of pytest, so let's go with that...

import networkx as nx
# extend Graph and DiGraph with our files, and create class DAG

def test_is_nonnull():
	nonnull = nx.Graph()
	nonnull.add_node('a')
	assert nonnull.is_nonnull()

	nonnull = nx.Graph()
	nonnull.add_edge('s', 't')
	assert nonnull.is_nonnull()

	nonnull = nx.Graph()
	assert nonnull.is_nonnull() == False





