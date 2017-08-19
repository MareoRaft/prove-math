from collections import OrderedDict

from lib.helper import *

def test_increment_string_counter():
	assert increment_string_counter('word') == 'word2'
	assert increment_string_counter('word0') == 'word1'
	assert increment_string_counter('word1') == 'word2'
	assert increment_string_counter('word764') == 'word765'

def test_json_import():
	# TODO
	pass

def test_json_export():
	# TODO
	pass

def test_strip_underscores():
	# TODO
	pass

def test_flatten_list_of_lists():
	l = []
	assert flatten_list_of_lists(l) == l

	l = [6, "four"]
	assert flatten_list_of_lists(l) == l

	l = [[]]
	assert flatten_list_of_lists(l) == []

	l = ["one", "two", ["three", "four"], ["five"], "six", ["seven"]]
	assert flatten_list_of_lists(l) == ["one", "two", "three", "four", "five", "six", "seven"]

def test_append_value_to_key():
	d = dict()
	append_value_to_key(d, "key", "value")
	assert d == {"key": {"value"}}

	d = {"key": {"value"}}
	append_value_to_key(d, "key", "value")
	assert d == {"key": {"value"}}

	d = {"key": {"value"}}
	append_value_to_key(d, "key", "value2")
	assert d == {"key": {"value", "value2"}}

	d = dict()
	append_value_to_key(d, ["k1", "k2"], "value", unpack_key=True)
	assert d == {"k1": {"value"}, "k2": {"value"}}

	d = {"k1": {"v1", "v2"}}
	append_value_to_key(d, ["k1", "k2", "k3"], "v2", unpack_key=True)
	assert d == {
		"k1": {"v1", "v2"},
		"k2": {"v2"},
		"k3": {"v2"},
	}

def test_reversed_dict():
	d = dict()
	assert reversed_dict(d) == dict()

	d = {"k": "v"}
	assert reversed_dict(d) == {"v": {"k"}}

	d = {"a": "v", "b": "v"}
	assert reversed_dict(d) == {"v": {"a", "b"}}

	d = {"k": ["a", "b"]}
	assert reversed_dict(d, unpack_values=True)  == {
		"a": {"k"},
		"b": {"k"},
	}

	d = {
		"k": ["a", "b"],
		"a": "v",
		"b": "v",
		"t": {"z", "k", "v"},
	}
	e = reversed_dict(d, unpack_values=True)
	assert e == {
		"a": {"k"},
		"b": {"k"},
		"v": {"a", "b", "t"},
		"z": {"t"},
		"k": {"t"},
	}
	f = reversed_dict(e, unpack_values=True)
	assert f == {
		"k": {"a", "b"},
		"a": {"v"},
		"b": {"v"},
		"t": {"z", "k", "v"},
	}


def test_DictToObject():
	# TODO
	pass

def test_render_content():
	content = 'hi *there*'
	correct_rendered_content = '<p>hi <em>there</em></p>'
	assert render_content(content) == correct_rendered_content

	content = '__underline__, *italic*, **bold**, _nothing_, and a <span>span</span>.'
	correct_rendered_content = '<p><u>underline</u>, <em>italic</em>, <strong>bold</strong>, _nothing_, and a <span>span</span>.</p>'
	assert render_content(content) == correct_rendered_content

	content = '\\['
	correct_rendered_content = '<p>\\[</p>'
	assert render_content(content) == correct_rendered_content

	content = '''
\\[this is display math\\]
$$this is display math$$'''
	correct_rendered_content = '''<p>\\[this is display math\\]<br />$$this is display math$$</p>'''
	assert render_content(content) == correct_rendered_content

	content = '''line one
line two'''
	correct_rendered_content = '''<p>line one<br />line two</p>'''
	assert render_content(content) == correct_rendered_content



