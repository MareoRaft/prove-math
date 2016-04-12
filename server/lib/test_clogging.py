from lib import clogging

def test_getLogger():
	# see if it actually gives you a logger
	l = clogging.getLogger('mylogger')
	l.warn('i\'m warning you!')
