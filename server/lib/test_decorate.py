import pytest

from lib.decorate import *

def test_read_only():
	class BlaBla:
		def __init__(self, value):
			self.v = value
		@property
		def v(self):
			return self._v
		@v.setter
		@read_only
		def v(self, new_value):
			self._v = new_value

	# verify we can set v the first time
	b = BlaBla("hello")
	assert b.v == "hello"

	# verify we CAN'T set v twice
	b = BlaBla("hello")
	with pytest.raises(Exception):
		b.v = "goodbye"
