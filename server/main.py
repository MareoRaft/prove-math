#!/usr/bin/env python3
################################# IMPORTS #####################################
import sys
import json
from warnings import warn
import pdb

from tornado.ioloop import IOLoop
from tornado.web import url # constructs a URLSpec for you
# handlers
from tornado.web import RedirectHandler
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler
# other
from tornado.web import Application
#from tornado.log import enable_pretty_logging

from lib import helper
from lib.mongo import Mongo
import networkx as nx
from lib.networkx.classes import dag

################################# HELPERS #####################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

def find_dict_from_id(list_of_dics, ID):
	for dic in list_of_dics:
		if dic['_id'] == ID:
			return dic
	# if the id doesn't exist, make a fake node...
	warn('Could node find dict with ID "' + ID + '" within list_of_dics.')
	return {"_id": ID, "empty": True, "_importance": 4}


################################## MAIN #######################################

class BaseHandler (RequestHandler):
	def initialize(self, var):
		#init stuff!
		print( var )
		pass
	def get(self, num):
		self.write("this is "+num+"!")

class FormHandler (BaseHandler):
	def get(self):
		# / is relative
		self.write("""	<form action='/form' method='post'>
							<input type='text' name='thisistheonlyinput' />
							<input type='submit' value='Submit' />
						</form>
					""")
	def post(self):
		invar = self.get_body_argument("thisistheonlyinput")
		print( "going to post the input!"+invar )

# The WebSocket protocol is still in development. This module currently implements the "hixie-76" and "hybi-10" versions of the protocol. See this browser compatibility table on Wikipedia: http://en.wikipedia.org/wiki/WebSockets#Browser_support
class SocketHandler (WebSocketHandler):
	def open(self):
		print('websocket opened!')

		# graph = { # python dictionary
		# 	'nodes': [
		# 		{'x': 40,  'y': 40}, # 0 is the index of this node
		# 		{'x': 80,  'y': 80}, # 1
		# 		{'x': 160, 'y': 160}, # 2
		# 		{'x': 0,   'y': 20}, # 3
		# 	],
		# 	'links': [
		# 		{'source': 0, 'target': 1, 'fixed': True, },
		# 		{'source': 2, 'target': 3},
		# 		{'source': 3, 'target': 1},
		# 	],
		# }

		# get appropriate subgraph from NewtorkX!
		global all_nodes
		global our_DAG
		graph = dict()
		graph['nodes'] = [find_dict_from_id(all_nodes, dict_id) for dict_id in our_DAG.nodes()]
		graph['links'] = [{'source': source, 'target': target} for (source, target) in our_DAG.edges()]

		# send to the user!
		bundled_graph = json.dumps(graph) # for the future, the following may be faster: 1. simplejason or 2. cjson
		self.write_message(bundled_graph)


	def on_message(self, message):
		print('got message: ' + message)
		# # ALL messages should come in as json strings
		# message = json.loads(message)
		# # ALL messages have a command that tells you what to do
		# # if the command is to add a new theorem, do it:
		# if message.command == 'new_node':
		# 	dic = message.dic
		# 	if 'importance' in dic.keys():
		# 		dic['importance'] = int(dic['importance'])
		# 	new_node = lib.node.create_appropriate_node(dic)
		# 	print('new node made.  looks like: '+new_node+'.  Now time to put it into the DB...')
		# 	global our_mongo
		# 	our_mongo.insert_single(new_node.__dict__)
		# # This can be placed in a try/exception block
		# # try:
		# #except Exception as e:
		# #	print("Unexpected error "+str(type(e)))
		# #	print(e)

	def on_close(self):
		print('A websocket has been closed.')


class StaticCachelessFileHandler(StaticFileHandler):


	def set_extra_headers(self, path):
		# Disable cache
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


def make_app():
	return Application(
		[
			url('/', RedirectHandler, { "url": "index.html" }, name = "rootme"),
			url(r'/here(\d)', BaseHandler, { "var": "tar" }, name = "here"), # regex quote!
			url('/form', FormHandler, { "var": "initialize this!" }, name = "forlorn"),
			url('/websocket', SocketHandler),
			url('/(.*)', StaticCachelessFileHandler, { "path": "../www/" }), # captures anything at all, and serves it as a static file. simple!
		],
		# settings:
		debug = True,
	)

def make_app_and_start_listening():
	#enable_pretty_logging()
	application = make_app()
	application.listen(80) # by listening on the http port (default for all browsers that i know of), user will not have to type "http://" or ":80" in the URL
	# other stuff
	IOLoop.current().start()


if __name__ == "__main__":
	# 1. grab nodes and edges from database
	all_nodes = list(Mongo("provemath", "nodes").find())
	all_edges = list(Mongo("provemath", "edges").find())

	# 2. create a networkx graph with the info...
	our_DAG = nx.DAG()
	our_DAG.add_nodes_from([node['_id'] for node in all_nodes])
	our_DAG.add_edges_from([(edge['source'], edge['target']) for edge in all_edges])
	print('The nodes are:')
	print(our_DAG.nodes())
	print()
	print('The edges are:')
	print(our_DAG.edges())
	print()
	# our_DAG.remove_redundant_edges()

	# 3. launch!
	make_app_and_start_listening()

