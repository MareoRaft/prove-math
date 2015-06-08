#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')
###############################################################################

import networkx as nx

class Graph (nx.Graph):
	def is_nonnull(self):
		return bool(self.nodes())

	def is_null(self):
		return not self.is_nonnull()

nx.Graph = Graph
