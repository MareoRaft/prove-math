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
# from tornado.log import enable_pretty_logging

from lib import helper
from lib.mongo import Mongo
import networkx as nx
from lib.networkx.classes import dag
from lib import user
import oauth_helper

################################# HELPERS #####################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

################################## MAIN #######################################


class BaseHandler (RequestHandler):


	def initialize(self, var):
		#init stuff!
		print( var )
		pass
	def get(self, num):
		self.write("this is "+num+"!")
		print(str(self.request))
		print()
		print(self.request.host)


class FormHandler (BaseHandler):


	def get(self):
		# / is relative
		urls=oauth_helper.initialize_login()

		self.write('<button id="FacebookManual" type="button">Facebook Manual</button><br><button id="GoogleManual" type="button">Google Manual</button><br><button id="LinkedinManual" type="button">Linkedin Manual</button> <br><button id="GithubManual" type="button">Github Manual</button><br><button id="TwitterManual" type="button">Twitter Manual</button><br> <script> document.getElementById("FacebookManual").onclick = function () {location.href ="'+urls['facebook']+'";};document.getElementById("GoogleManual").onclick = function () {location.href ="'+urls['google']+'";};document.getElementById("LinkedinManual").onclick = function () {location.href ="'+urls['linkedin']+'";};document.getElementById("GithubManual").onclick = function () {location.href ="'+urls['github']+'";};</script>')

	def post(self):
		invar = self.get_body_argument("thisistheonlyinput")
		print( "going to post the input!"+invar )


class HomeHandler(BaseHandler):


	def get(self):


		method=self.get_argument("method", default=None, strip=False)
		authorization_code=self.get_argument("code", default=None, strip=False)
		redirect_response='https://localhost/home?method='+method+'&code='+authorization_code

		if method=='fb':
			obj=oauth_helper.get_facebook_oauth()
		elif method=='google':
			obj=oauth_helper.get_google_oauth()
		elif method=='linkedin':
			obj=oauth_helper.get_linkedin_oauth()
		elif method=='github':
			obj=oauth_helper.get_github_oauth()

		obj.oauth_obj.fetch_token(obj.token_url, client_secret=obj.secret,authorization_response=redirect_response)
		r=obj.oauth_obj.get(obj.request_url)
		self.write('<h2>Welcome '+str(r.content)+'</h2> <br> <h2> Your access token is </h2>')

	def post(self):
		invar = self.get_body_argument("thisistheonlyinput")
		print( "going to post the input!"+invar )



class JSONHandler (BaseHandler):


	def get(self):
		# get appropriate subgraph from NewtorkX!
		global all_nodes
		global our_DAG
		json_graph = our_DAG.as_complete_json(all_nodes)

		# send to the user!
		self.write(json_graph)




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
		dict_graph = our_DAG.as_complete_dict(all_nodes)

		self.write_message({ # write_message uses json by default!
			'command': 'load-graph',
			'new_graph': dict_graph,
		})

	def on_message(self, message): # here, however, we must json.loads it ourselves...
		print('got message: ' + message)
		ball = json.loads(message)
		if ball['command'] == 'print':
			print(ball['message'])
		elif ball['command'] == 'learn-node':
			# get associated user somehow?
			user.learn_node(ball['node_id'])
		elif ball['command'] == 'unlearn-node':
			# ditto
			user.unlearn_node(ball['node_id'])
		elif ball['command'] == 'set-pref':
			# ditto
			user.set_pref(ball['pref_dict'])

		# if ball['command'] == 'new_node':
		# 	node_dict = ball['dict']
		# 	if 'importance' in node_dict.keys():
		# 		node_dict['importance'] = int(node_dict['importance'])
		# 	new_node = lib.node.create_appropriate_node(node_dict)
		# 	print('new node made.  looks like: '+new_node+'.  Now time to put it into the DB...')
		# 	global our_mongo
		# 	our_mongo.insert_single(new_node.__dict__)
		# This can be placed in a try/exception block
		# try:
		#except Exception as e:
		#	print("Unexpected error "+str(type(e)))
		#	print(e)

	def on_close(self):
		print('A websocket has been closed.')


class StaticCachelessFileHandler(StaticFileHandler):


	def prepare(self):
		if self.request.host != 'provemath.org' and self.request.host != 'localhost':
			self.redirect('http://provemath.org', self.request.uri)
			tornado.web.Finish()
	def set_extra_headers(self, path):
		# Disable cache
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


def make_app():
	return Application(
		[
			url('/', RedirectHandler, { "url": "index.html" }, name = "rootme"),
			url(r'/here(\d)', BaseHandler, { "var": "tar" }, name = "here"), # regex quote!
			url('/form', FormHandler, { "var": "initialize this!" }, name = "forlorn"),
			url('/websocket', SocketHandler),url('/home',HomeHandler, {"var":"test"}  ),
			url('/json', JSONHandler, { "var": "null" }, name = "jsonme"),
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
	our_DAG.remove_redundant_edges()

	# 3. launch!
	make_app_and_start_listening()

