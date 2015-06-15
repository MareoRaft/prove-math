#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
	raise SystemExit('Please use Python version 3.4 or above')

################################## MAIN #######################################
from tornado.ioloop import IOLoop
from tornado.web import url # constructs a URLSpec for you

from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler

from tornado.web import Application
from tornado.log import enable_pretty_logging
import json

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
		# get node json info
		# send it over!!
		# self.write_message()

	def on_message(self, message):
		print('got message: ' + message)
		# for the future, consider that these may be FASTER:
		# 	import simplejson as json
		# 	json.loads(obj) # first option
		# 	or
		# 	cjson.decode(obj) # second option
		graph = {
			'nodes': [
				{'x': 40,  'y': 40}, # 0 is the index of this node
				{'x': 80,  'y': 80}, # 1
				{'x': 160, 'y': 160}, # 2
				{'x': 0,   'y': 20}, # 3
			],
			'links': [
				{'source': 0, 'target': 1, 'fixed': True, },
				{'source': 2, 'target': 3},
				{'source': 3, 'target': 1},
			],
		}
		bundled = json.dumps(graph)
		self.write_message(bundled)

	def on_close(self):
		print('websocket closed')




def make_app():
	return Application(
		[
			url('/', BaseHandler, { "var":"nothing" }, name="root"), # this is for the root! :)
			url(r'/here(\d)', BaseHandler, { "var":"tar" }, name = "here"), # regex quote!
			url('/form', FormHandler, { "var":"initialize this!" }, name = "forlorn"),
			url('/websocket', SocketHandler),
			url('/(.*)', StaticFileHandler, { "path":"../www/" }), # captures anything at all, and serves it as a static file. simple!
		],
		# settings:
		debug = True,
	)


def main():
	enable_pretty_logging()
	application = make_app()
	application.listen(80) # by listening on the http port (default for all browsers that i know of), user will not have to type "http://" or ":80" in the URL
	# other stuff
	IOLoop.current().start()

if __name__ == "__main__": main()

