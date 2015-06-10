#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')
###############################################################################

import networkx as nx

class _GraphExtended (nx.Graph):
	def is_nonnull(self):
		return bool(self.nodes())

	def is_null(self):
		return not self.is_nonnull()




# for key in _GraphExtended.__dict__:
for key, value in _GraphExtended.__dict__.items():
	try:
		# nx.Graph.is_nonnull = _GraphExtended.is_nonnull
		setattr(nx.Graph, key, value)
	except TypeError:
		pass


# nx.Graph.is_nonnull = _GraphExtended.is_nonnull
# print(_GraphExtended.__dict__)
# except TypeError as e:
# 	print(str(e))
