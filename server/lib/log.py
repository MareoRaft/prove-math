""" This is a wrapper around the built-in logging module with some extra goodies added with chromalog and a convenient usage.

To use in any module, just type `log.debug('my message')` or `log.warn('my message')`, etc.
"""
import chromalog
import logging
import time

from lib import decorate


# make 'debug' messages green (like 'success' messages)
debug = chromalog.colorizer.Colorizer.default_color_map['debug'] # remember debug's color, in case we want it later
success = chromalog.colorizer.Colorizer.default_color_map['success']
chromalog.colorizer.Colorizer.default_color_map['debug'] = success

""" # Retrieve a logger for use!  For example:

# from chromalog.mark.helpers.simple import important

log.debug('this message is for %s purposes', important('debugging'))
log.info('this is a regular info message')
log.warning('this message is some warning')
"""

chromalog.basicConfig(level=logging.DEBUG, format='%(asctime)s   %(filename)s line %(lineno)d   %(levelname)s:   %(message)s', datefmt='%Y-%m-%d at %I:%M %p and %S secs')
logger = logging.getLogger()
# say hi!
logger.debug("Hi, there!  I'm ready to log!")

# expose some logger methods:
def debug(*args, **kwargs):
	logger.debug(*args, **kwargs)

def info(*args, **kwargs):
	logger.info(*args, **kwargs)

def important(*args, **kwargs):
	logger.important(*args, **kwargs)

def success(*args, **kwargs):
	logger.success(*args, **kwargs)

def warning(*args, **kwargs):
	logger.warning(*args, **kwargs)

def error(*args, **kwargs):
	logger.error(*args, **kwargs)

def critical(*args, **kwargs):
	logger.critical(*args, **kwargs)

# create some logging decorators :)
@decorate.transparent
def elapsed_time(func):
	def new_func(*args, **kwargs):
		start_time = time.time()
		out = func(*args, **kwargs)
		elapsed_time = time.time() - start_time
#		log_msg = time.ctime() + '\tFunction: ' + func.__name__ + '\tRuntime: ' + str(elapsed_time)
		log_msg = 'Function: ' + func.__name__ + '\tRuntime: ' + str(elapsed_time)
		#print(log_msg)
		info(log_msg)
		return out
	return new_func

