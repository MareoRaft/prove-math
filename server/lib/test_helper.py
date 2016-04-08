from lib.helper import *

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

def test_reverse_dict():
    d = dict()
    assert reverse_dict(d) == dict()

    d = {"k": "v"}
    assert reverse_dict(d) == {"v": {"k"}}

    d = {"a": "v", "b": "v"}
    assert reverse_dict(d) == {"v": {"a", "b"}}

    d = {"k": ["a", "b"]}
    assert reverse_dict(d, unpack_values=True)  == {
        "a": {"k"},
        "b": {"k"},
    }

    d = {
        "k": ["a", "b"],
        "a": "v",
        "b": "v",
        "t": {"z", "k", "v"},
    }
    e = reverse_dict(d, unpack_values=True)
    assert e == {
        "a": {"k"},
        "b": {"k"},
        "v": {"a", "b", "t"},
        "z": {"t"},
        "k": {"t"},
    }
    f = reverse_dict(e, unpack_values=True)
    assert f == {
        "k": {"a", "b"},
        "a": {"v"},
        "b": {"v"},
        "t": {"z", "k", "v"},
    }

def test_DictToObject():
    # TODO
    pass

