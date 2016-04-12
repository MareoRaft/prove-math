""" clogging = custom logging
This is a wrapper around the built-in logging module with some custom defaults and color support via colorlog.

Usage:
import clogging
log = clogging.getLogger('somename')
log.debug('my message') or log.warning('my message'), etc.
"""
import logging
import colorlog

FORMAT_TEMPLATE = '%(asctime)s  %(filename)s line %(lineno)d  {}%(levelname)s{}: {}%(message)s'
FORMAT_DEFAULT = FORMAT_TEMPLATE.format('', '', '')
FORMAT_COLOR = FORMAT_TEMPLATE.format('%(log_color)s', '%(reset)s', '%(message_log_color)s')
DATEFMT = '%Y-%m-%d %I:%M %p %S secs'

def getLogger(name, filename=None, stdout=True):
	# in the future, when logging gets more complex, consider using a hierarchy of loggers and stuff like
	# getChild and make child, etc, to deal with it: https://docs.python.org/3.5/library/logging.html
	if name in logging.Logger.manager.loggerDict: # (if the logger already exists)
		return logging.getLogger(name)
	else:
		# build our own "custom defaults" logger
		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG) # if you want to see more than just warnings, remember this!!  You can also set this option to a HANDLER if you want that handler to be at a different level.
		if stdout:
			stdout_handler = logging.StreamHandler()
			stdout_handler.setFormatter(
				colorlog.ColoredFormatter(
					FORMAT_COLOR,
					datefmt=DATEFMT,
					log_colors={
						'DEBUG':    'cyan',
						'INFO':     'green',
						'WARNING':  'yellow',
						'ERROR':    'red',
						'CRITICAL': 'red,bg_white',
					},
					secondary_log_colors={ # use with %(message_log_color)s
						'message': {
							'ERROR':    'red',
							'CRITICAL': 'red'
						}
					},
				)
			)
			logger.addHandler(stdout_handler)
		if filename is not None:
			fh = logging.FileHandler(filename)
			fh.setFormatter(
				logging.Formatter(
					FORMAT_DEFAULT,
					datefmt=DATEFMT
				)
			)
			logger.addHandler(fh)
		return logger
