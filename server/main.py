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

#Oauth
import requests
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
		facebook=oauth_helper.facebook_oauth()
		google=oauth_helper.google_oauth()
		linkedin=oauth_helper.linkedin_oauth()
		github=oauth_helper.github_oauth()

		fb_authorization_url, state = facebook.authorization_url('https://www.facebook.com/dialog/oauth')
		google_authorization_url, state = google.authorization_url("https://accounts.google.com/o/oauth2/auth",access_type="offline", approval_prompt="force")
		linkedin_authorization_url, state = linkedin.authorization_url('https://www.linkedin.com/uas/oauth2/authorization')
		github_authorization_url, state = github.authorization_url('https://github.com/login/oauth/authorize')
		self.write('<button id="FacebookManual" type="button">Facebook Manual</button><br><button id="GoogleManual" type="button">Google Manual</button><br><button id="LinkedinManual" type="button">Linkedin Manual</button> <br><button id="GithubManual" type="button">Github Manual</button><br><button id="TwitterManual" type="button">Twitter Manual</button><br> <script> document.getElementById("FacebookManual").onclick = function () {location.href ="'+fb_authorization_url+'";};document.getElementById("GoogleManual").onclick = function () {location.href ="'+google_authorization_url+'";};document.getElementById("LinkedinManual").onclick = function () {location.href ="'+linkedin_authorization_url+'";};document.getElementById("GithubManual").onclick = function () {location.href ="'+github_authorization_url+'";};</script>')
		
	def post(self):
		invar = self.get_body_argument("thisistheonlyinput")
		print( "going to post the input!"+invar )

class HomeHandler(BaseHandler):
	def get(self):
		secrets=oauth_helper.get_secrets()
		fb_client_secret=secrets[0]
		google_client_secret=secrets[1]
		linkedin_client_secret=secrets[2]
		github_client_secret=secrets[3]

		method=self.get_argument("method", default=None, strip=False)
		authorization_code=self.get_argument("code", default=None, strip=False)

		facebook=oauth_helper.facebook_oauth()
		google=oauth_helper.google_oauth()
		linkedin=oauth_helper.linkedin_oauth()
		github=oauth_helper.github_oauth()

		if method=='fb':
			fb_token_url = 'https://graph.facebook.com/oauth/access_token'
			redirect_response='https://localhost/home?method=fb&code='+authorization_code
			facebook.fetch_token(fb_token_url, client_secret=fb_client_secret, authorization_response=redirect_response)
			r=facebook.get('https://graph.facebook.com/me?')
			self.write('<h2>Welcome '+str(r.content)+'</h2> <br> <h2> Your access token is '+facebook.token['access_token']+'</h2>')

		elif method=='google':
			google_token_url="https://accounts.google.com/o/oauth2/token"
			redirect_response='https://localhost/home?method=google&code='+authorization_code
			google.fetch_token(google_token_url,client_secret=google_client_secret,authorization_response=redirect_response)
			r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
			self.write('<h2>Welcome '+str(r.content)+'</h2> <br> <h2> Your access token is </h2>')
		elif method=='linkedin':
			linkedin_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
			redirect_response='https://localhost/home?method=linkedin&code='+authorization_code
			linkedin.fetch_token(linkedin_token_url, client_secret=linkedin_client_secret,authorization_response=redirect_response)
			r = linkedin.get('https://api.linkedin.com/v1/people/~')
			self.write('<h2>Welcome '+str(r.content)+'</h2> <br> <h2> Your access token is </h2>')
		elif method=='github':
			github_token_url = 'https://github.com/login/oauth/access_token'
			redirect_response='https://localhost/home?method=github&code='+authorization_code
			github.fetch_token(github_token_url, client_secret=github_client_secret,authorization_response=redirect_response)
			r=github.get('https://api.github.com/user')
			self.write('<h2>Welcome '+str(r.content)+'</h2> <br> <h2> Your access token is </h2>')
	
		else:
			self.write('<h2> Login Error </h2>')
		
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
		json_graph = our_DAG.as_complete_json(all_nodes)

		# send to the user!
		self.write_message(json_graph)


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

