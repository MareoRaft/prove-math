#!/usr/bin/env python3
################################# IMPORTS #####################################
import sys
import json
from warnings import warn
import pdb

from tornado.ioloop import IOLoop
from tornado.web import url  # constructs a URLSpec for you
# handlers
from tornado.web import RedirectHandler
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler
# other
from tornado.web import Application
from tornado.web import Finish
from tornado.escape import xhtml_escape
# from tornado.log import enable_pretty_logging

from lib.mongo import Mongo
from lib.user import User
import networkx as nx
from lib.networkx.classes import dag
from lib import user
from lib import auth
# this and relevant code should eventually be migrated into auth module
import xml.etree.ElementTree as ET

################################# HELPERS #####################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

################################## MAIN #######################################


class BaseHandler(RequestHandler):

	def prepare(self):
		print('THE HOST IS: ' + self.request.host)
		if self.request.host != 'provemath.org' and self.request.host != 'localhost':
			self.redirect('http://provemath.org', self.request.uri)
			Finish()

	# this is for development only, and may not be needed when using incognito
	# mode anyway.  This must be commented out when moving to server.
	def set_extra_headers(self, path):
		# Disable cache
		self.set_header(
			'Cache-Control',
			'no-store, no-cache, must-revalidate, max-age=0')


class IndexHandler(BaseHandler):

	def get(self):
		method = self.get_argument("method", default=None, strip=False)
		authorization_code = self.get_argument("code", default=None, strip=False)
		if self.get_secure_cookie("mycookie"):
			user_dict=json.loads(str(self.get_secure_cookie("mycookie"),'UTF-8'))
			print("Welcome back user "+ user_dict['_id'])
			print("Now clearing you out")
			self.clear_cookie("mycookie")

		elif method is not None and authorization_code is not None:
			print('got params!!!!')
			redirect_response = 'https://' + self.request.host + \
				'/index?method=' + method + '&code=' + authorization_code
			provider = auth.get_new_provider(method)

			provider.oauth_obj.fetch_token(
				provider.token_url,
				client_secret=provider.secret,
				authorization_response=redirect_response
			)
			user_info = provider.oauth_obj.get(provider.request_url)

			if provider.request_format == 'json':
				r_text_dict = json.loads(user_info.text)
				account_id = r_text_dict['id']
			else:
				xml_root = ET.fromstring(user_info.text)
				account_id = xml_root.find('id').text

			user = User({'account_type': provider.name,
						 'account_id': account_id})
			print("logged_in.dict is: " + str(user.dict))
			user_dict = user.dict
			self.set_secure_cookie("mycookie",json.dumps(user_dict))
		else:
			user_dict={}
		self.render("../www/index.html",
					user_dict_json_string=json.dumps(user_dict),
					host=self.request.host
					)


class JSONHandler(BaseHandler):

	def get(self):
		# get appropriate subgraph from NewtorkX!
		global all_nodes
		global our_DAG
		json_graph = our_DAG.as_complete_json(all_nodes)

		# send to the user!
		self.write(json_graph)


# The WebSocket protocol is still in development. This module currently
# implements the "hixie-76" and "hybi-10" versions of the protocol. See
# this browser compatibility table on Wikipedia:
# http://en.wikipedia.org/wiki/WebSockets#Browser_support
class SocketHandler(WebSocketHandler):

	def open(self):
		print('websocket opened!')

		self.write_message({
			'command': 'populate-oauth-urls',
			'url_dict': auth.auth_url_dict(),
		})

		# get appropriate subgraph from NewtorkX!
		global all_nodes
		global our_DAG
		dict_graph = our_DAG.as_complete_dict(all_nodes)

		self.write_message({  # write_message uses json by default!
			'command': 'load-graph',
			'new_graph': dict_graph,
		})

	# here, however, we must json.loads it ourselves...
	def on_message(self, message):
		print('got message: ' + message)
		ball = json.loads(message)
		if ball['command'] == 'print':
			print(ball['message'])
		elif ball['command'] == 'learn-node':
			user = User(ball['identifier'])
			user.learn_node(ball['node_id'])
		elif ball['command'] == 'unlearn-node':
			user = User(ball['identifier'])
			user.unlearn_node(ball['node_id'])
		elif ball['command'] == 'set-pref':
			user = User(ball['identifier'])
			user.set_pref(ball['pref_dict'])

		# if ball['command'] == 'new-node':
		# 	node_dict = ball['dict']
		# 	if 'importance' in node_dict.keys():
		# 		node_dict['importance'] = int(node_dict['importance'])
		# 	new_node = lib.node.create_appropriate_node(node_dict)
		# 	print('new node made.  looks like: '+new_node+'.  Now time to put it into the DB...')
		# 	global our_mongo
		# 	our_mongo.insert_single(new_node.__dict__)
		# This can be placed in a try/exception block
		# try:
		# except Exception as e:
		#	print("Unexpected error "+str(type(e)))
		#	print(e)

	def on_close(self):
		print('A websocket has been closed.')


class StaticHandler(StaticFileHandler, BaseHandler):

	# A static file handler with our BaseHandler cachelessness and redirection.
	pass


def make_app():
	return Application(
		[
			url('/', RedirectHandler, {"url": "index.html"}, name="rooth"),
			url('/websocket', SocketHandler),
			url('/json', JSONHandler, name="jsonh"),
			url(r'/index(?:\.html)?', IndexHandler, name="indexh"),
			# captures anything at all, and serves it as a static file. simple!
			url(r'/(.*)', StaticHandler, {"path": "../www/"}),
		],
		# settings:
		debug=True,
		cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
	)


def make_app_and_start_listening():
	# enable_pretty_logging()
	application = make_app()
	# by listening on the http port (default for all browsers that i know of),
	# user will not have to type "http://" or ":80" in the URL
	application.listen(80)
	# other stuff
	IOLoop.current().start()


if __name__ == "__main__":
	# 1. grab nodes and edges from database
	all_nodes = list(Mongo("provemath", "nodes").find())
	all_edges = list(Mongo("provemath", "edges").find())

	# 2. create a networkx graph with the info...
	our_DAG = nx.DAG()
	our_DAG.add_nodes_from([node['_id'] for node in all_nodes])
	our_DAG.add_edges_from([(edge['source'], edge['target'])
							for edge in all_edges])
	print('Node array loaded with length: ' + str(len(our_DAG.nodes())))
	print('Edge array loaded with length: ' + str(len(our_DAG.edges())))
	our_DAG.remove_redundant_edges()

	# 3. launch!
	make_app_and_start_listening()
