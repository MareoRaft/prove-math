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

from networkx.readwrite import json_graph
from lib.helper import strip_underscores
from lib.node import create_appropriate_node
from lib.mongo import Mongo
from lib.user import User
import networkx as nx
from lib.networkx.classes import dag
from lib import user
from lib import auth
from lib import node
import random
import inspect
import traceback
from lib import log
# this and relevant code should eventually be migrated into auth module
import xml.etree.ElementTree as ET

################################# HELPERS #####################################
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

def random_string(length):
	word = ''
	for i in range(length):
		word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789')
	return word

################################## MAIN #######################################


class BaseHandler(RequestHandler):


	def prepare(self):
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
		user_dict = {}
		method = self.get_argument("method", default=None, strip=False)
		authorization_code = self.get_argument("code", default=None, strip=False)

		cookie = self.get_secure_cookie("mycookie")
		if cookie:
			print('COOKIE IS: '+str(cookie))
			user_identifier = json.loads(str(cookie, 'UTF-8'))
			print('user identifier IS: '+str(user_identifier))
			user = User(user_identifier)
			user_dict = user.dict # WHAT ABOUT THE PICTURE? maybe...
			# user_dict = provider.id_and_picture(request_root, user.dict)

		elif method is not None and authorization_code is not None:
			print('got params!!!!')
			redirect_response = 'https://' + self.request.host + \
				'/index?method=' + method + '&code=' + authorization_code
			provider = auth.get_new_provider(method, host=self.request.host)
			try:
				provider.oauth_obj.fetch_token(
					provider.token_url,
					client_secret=provider.secret,
					authorization_response=redirect_response
					)
				user_info = provider.oauth_obj.get(provider.request_url)

				if provider.request_format == 'json':
					request_root = json.loads(user_info.text)
					account_id = request_root['id']
				else:
					request_root = ET.fromstring(user_info.text)
					account_id = request_root.find('id').text
				user = User({
					'type': provider.name,
					'id': account_id
				})
				user_dict = provider.id_and_picture(request_root, user.dict)
				print("logged in dict is:"+ str(user_dict)+"\n")
				self.set_secure_cookie("mycookie", json.dumps(user.identifier))
			except Exception as e:
				print('Login failed.  Exception message below:')
				print(e) # user_dict is still {}
				# inspect.stack()
				(typ, val, tb) = sys.exc_info()
				traceback.print_tb(tb)

		else:
			pass # user not logged in

		self.render("../www/index.html",
					user_dict_json_string=json.dumps(user_dict),
					host=self.request.host,
					subjects=json.dumps(list(starting_nodes.keys()))
					)


class JSONHandler(BaseHandler):


	def get(self):
		# get appropriate subgraph from NewtorkX!
		json_graph = our_DAG.as_complete_json() # TODO write this method
		self.write(json_graph)


# The WebSocket protocol is still in development. This module currently
# implements the "hixie-76" and "hybi-10" versions of the protocol. See
# this browser compatibility table on Wikipedia:
# http://en.wikipedia.org/wiki/WebSockets#Browser_support
class SocketHandler (WebSocketHandler):


	def __init__(self, application, request, **kwargs):
		WebSocketHandler.__init__(self, application, request, **kwargs)
		self.user = None

	def jsend(self, dic):
		if self.user:
			user_identifier = self.user.dict['account']
			dic['identifier'] = user_identifier
		else:
			dic['identifier'] = None
		self.write_message(dic)

	def open(self):
		# this happens BEFORE first-steps
		self.jsend({
			'command': 'populate-oauth-urls',
			'url_dict': auth.auth_url_dict(host=self.request.host),
		})

	def on_message(self, message):
		log.debug('got message: ' + message+"\n")
		ball = json.loads(message)

		if ball['command'] == 'print':
			print(ball['message'])

		elif ball['command'] == 'first-steps':
			self.user = User(ball['identifier'])
			self.jsend({'command': 'update-user'})
			if self.ids(ball):
				self.send_graph(ball)
			else: # they've learned nothing yet
				self.jsend({
					'command': 'prompt-starting-nodes',
				})

		elif ball['command'] == 'get-starting-nodes':
			subject = ball['subject']
			self.send_graph(ball, subject)

		elif ball['command'] == 'learn-node':
			self.user.learn_node(ball['node_id'])
			if ball['mode'] == 'learn':
				self.send_graph(ball)
			else:
				raise Exception('mode is not learn')

		elif ball['command'] == 'unlearn-node':
			self.user.unlearn_node(ball['node_id'])

		elif ball['command'] == 'set-pref':
			self.user.set_pref(ball['pref_dict'])

		elif ball['command'] == 'save-node': # hopefully this can handle both new nodes and changes to nodes
			node_dict = ball['node_dict']
			if 'importance' in node_dict.keys():
				node_dict['importance'] = int(node_dict['importance'])
			try:
				node_obj = node.create_appropriate_node(node_dict)
				log.debug('\nnode made.  looks like: '+str(node_obj)+'.  Now time to put it into the DB...\n')
				# take a look at the dependencies now

				# TODO if the node is brand new (mongo can't find it), then let previous_dep_ids = []
				previous_dependency_ids = [node.reduce_string(dependency) for dependency in list(our_mongo.find({"_id": node_obj.id}))[0]["_dependencies"]] # if this works, try using set() instead of list and elimination the set()s below
				log.debug('prev deps are: '+str(previous_dependency_ids))
				current_dependency_ids = node_obj.dependency_ids
				log.debug('curr deps are: '+str(current_dependency_ids))
				new_dependency_ids = set(current_dependency_ids) - set(previous_dependency_ids)
				removed_dependency_ids = set(previous_dependency_ids) - set(current_dependency_ids)


				# VERIFY THAT THE GRAPH WITH THESE NEW ARCS IS STILL ACYCLIC:
				H = our_DAG.copy()
				for new_dependency_id in new_dependency_ids:
					print('from '+str(our_DAG.n(new_dependency_id))+' to '+str(node_obj))
					H.add_edge(new_dependency_id, node_obj.id)
					H.validate(node_obj.name + ' cannot depend on ' + our_DAG.n(new_dependency_id).name + ' because ' + our_DAG.n(new_dependency_id).name + ' already depends on ' + node_obj.name + '!')

				our_mongo.upsert({ "_id": node_obj.id }, node_obj.__dict__)
				update_our_DAG()

				# send an update of the graph to the user if there are new dependencies:
				self.request_nodes(new_dependency_ids, ball)
				self.remove_client_edges(node_obj.id, removed_dependency_ids)
			except Exception as error:
				# stuff didn't work, send error back to user
				log.warning('ERROR: '+str(error))
				self.jsend({
					'command': 'display-error',
					'message': str(error),
				})

		elif ball['command'] == 're-center-graph':
			# We get the 5th nearest neighbors
			neighbors = our_DAG.single_source_shortest_anydirectional_path_length(ball['central_node_id'], 1)
			H = our_DAG.subgraph(list(neighbors.keys()))
			dict_graph = H.as_complete_dict()
			self.jsend({
				'command': 'load-graph',
				'new_graph': dict_graph,
			})

		elif ball['command'] == 'request-node':
			self.request_nodes([ball['node_id']], ball)

		elif ball['command'] == 'search':
			search_results = our_mongo.find({'$text':{'$search':ball['search_term']}},{'score':{'$meta':"textScore"}})
			self.jsend({
					'command': 'search-results',
					'results': list(search_results.sort([('score', {'$meta': 'textScore'})]).limit(10)),
			})

	def request_nodes(self, node_ids, ball):
		for node_id in node_ids:
			if node_id not in our_DAG.nodes():
				raise ValueError('The node_id "'+node_id+'" does not exist.')
		ids = set(self.user.dict['learned_node_ids']).union(set(ball['client_node_ids'])).union(set(node_ids))
		H = our_DAG.subgraph(list(ids))
		dict_graph = H.as_complete_dict()
		self.jsend({
			'command': 'load-graph',
			'new_graph': dict_graph,
		})

	def remove_client_edges(self, node_id, dependency_ids):
		self.jsend({
			'command': 'remove-edges',
			'node_id': node_id,
			'dependency_ids': list(dependency_ids),
		})

	def ids(self, ball):
		learned_ids = self.user.dict['learned_node_ids']
		return list(set(learned_ids).union(set(ball['client_node_ids'])))

	def send_graph(self, ball, subject=None):
		log.debug('SUBJECT IS: ' + subject)
		log.debug('LOGGED IN AS: ' + str(self.user.identifier))
		ids = self.ids(ball)
		if ids:
			learned_ids = self.user.dict['learned_node_ids']
			ids_to_send = our_DAG.absolute_dominion(learned_ids)
			ids_to_send = set(ids_to_send).union(set(ids)).union(set(self.other_nodes_of_interest(subject)))
			H = our_DAG.subgraph(list(ids_to_send))
		else:
			# they've learned nothing so far.  send them a starting point
			H = our_DAG.subgraph(self.starting_nodes(subject))

		dict_graph = H.as_complete_dict()
		self.jsend({
			'command': 'load-graph',
			'new_graph': dict_graph,
		})

	def other_nodes_of_interest(self, subject=None):
		# but instead of sending ALL sources, let's look for deepest/most bang for buck, and send relevant sources of THAT
		nodes = []
		if subject:
			nodes = nodes + self.starting_nodes(subject)
		return nodes
		# for later, add the following too:
		return [our_DAG.short_sighted_depth_first_unlearned_source(starting_nodes, learned_ids)]

	def starting_nodes(self, subject):
		return starting_nodes[subject]

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
		cookie_secret=random_string(99)
	)

def make_app_and_start_listening():
	# enable_pretty_logging()
	application = make_app()
	application.listen(80)
	# other stuff
	IOLoop.current().start()

def update_our_DAG():
	# 1. grab nodes and edges from database
	all_node_dicts = list(Mongo("provemath", "nodes").find())

	# 2. create a networkx graph with the info...
	global our_DAG
	our_DAG = nx.DAG()
	for node_dict in all_node_dicts:
		try:
			node = create_appropriate_node(strip_underscores(node_dict))
		except Exception as e:
			print('\nerror.  could not create_appropriate_node.  node_dict was: '+str(strip_underscores(node_dict)))
		our_DAG.add_n(node)
	for node_id in our_DAG.nodes():
		node = our_DAG.n(node_id)
		for dependency_id in node.dependency_ids:
			our_DAG.add_edge(dependency_id, node_id)
	our_DAG.validate() # make sure it's still Acyclic
	print('Node array loaded with length: ' + str(len(our_DAG.nodes())))
	print('Edge array loaded with length: ' + str(len(our_DAG.edges())))
	our_DAG.remove_redundant_edges()

if __name__ == "__main__":
	# 0. create a global mongo object for later use (for upserts in the future)
	our_mongo = Mongo("provemath", "nodes")

	# 1 and 2
	update_our_DAG()
	starting_nodes = {
		'graph theory': ['set', 'multiset', 'vertex'],
		'combinatorics': ['set', 'multiset', 'identical', 'factorial', 'finiteset'],
		'category theory': ['equatable', 'type'],
	}

	# 3. launch!
	make_app_and_start_listening()
#stupid comment
