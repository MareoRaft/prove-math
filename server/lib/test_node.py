import sys
import pytest
from lib.node import create_appropriate_node
from lib.node import Definition
from lib.node import Theorem
from lib.node import Exercise

sample_theorem = {
  "name": "Pythagorean theorem",
  "weight": 8,
  "thm": "The relationship between the legs, a and b of a right triangle and the hypotenuse, c, is $a^2b^2=c^2$.",
  "intuition": "A simple explanation",
  "examples": ["Example 1 is long enough", "Example 2 is long enough"]
}


##########################INIT, SETTERS/GETTERS, ATTRIBUTE TESTS################

def test_theorem_copy():
  global sample_theorem
  a = create_appropriate_node(sample_theorem)
  assert isinstance(a, Theorem)

  b = a.clone()
  assert id(a) != id(b)
  assert a == b


def test_theorem_setter_getter():
  pre_node = {
    "name": "Pythagorean theorem",
    "weight": 6,
    "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.",
    "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],
    "type": "theorem",
    "proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Theorem)

  assert node.name == "Pythagorean theorem"
  assert node.type == "theorem"
  assert node.importance == 6
  assert node.description == "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2."
  assert node.intuitions == ["A simple explanation."]
  assert node.examples ==  ["Example 1 is now long enough.", "Example 2 is now long."]
  assert node.proofs ==  [{"type": ["fake"], "description": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}]

def test_theorem_bad_attributes():
  pre_node = {
    "name": "Pythagorean theorem",
    "plural": "yo",
    "weight": 6,
    "theorem": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.",
    "intuition": "A simple explanation.",
    "examples": ["Example 1 is now long enough.", "Example 2 is now long."],
    "proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Theorem)

  # with pytest.raises(AssertionError): # TODO TODO TODO
  #   node.intuition = "longer longer 3^2+4^2=5^2"
  # with pytest.raises(Exception): # or some more specific error.  this is a TODO (see stack overflow)
    # node.chicken = "some plural"

def test_exercise_setter_getter():
  pre_node = {
    "weight": 2,
    "exercise": "Three Four Five Triangle",
    "intuition": "Longer longer 3^2+4^2=5^2",
    "examples": ["Example 1 is now long enough.", "Example 2 is now long."],
    "proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Exercise)

  print(node)
  assert node.name == None
  assert node.type == "exercise"
  assert node.importance == 2
  assert node.description == "Three Four Five Triangle"

def test_exercise_bad_attributes():
  pre_node = {
    "weight": 2,
    "description": "Three Four Five Triangle",
    "intuition": "3^2+4^2=5^2",
    "examples": ["Example 1 is now long enough.", "Example 2 is now long."],
    "proof": {
      "type": "fake",
      "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."
    }
  }
  with pytest.raises(KeyError):
    node = create_appropriate_node(pre_node) # there should be an error because pre_node has no type

def test_exercise_adding_a_plural():
  pre_node = {
    "type": "exercise",
    "weight": 2,
    "description": "Three Four Five Triangle",
    "examples": ["Example 1 is now long enough.", "Example 2 is now long."],
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Exercise)

  with pytest.raises(AttributeError): # simple because the attribute doesn't exist
    node.plural == ""

def test_definition_setters_getters():
  pre_node = {
    "name": "Custom Name",
    "weight": 1,
    "def": "A __triangle__ is a 3 sided polygon.",
    "plural": "__triangles__",
    "intuition": "A simple explanation",
    "examples": ["Long Long Long Example 1", "text text text Example 2"]
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Definition)

  assert node.name == "Custom Name"
  assert node.type == "definition"
  assert node.importance == 1
  assert node.description == "A __triangle__ is a 3 sided polygon."
  assert node.plural == "__triangles__"
  assert node.examples == ["Long Long Long Example 1", "text text text Example 2"]


def test_definition_bad_attributes():
  sample_definition = {
    "name": "Triangle",
    "weight": 1,
    "definition": "A __triangle__ is a 3 sided polygon.",
    "intuition": "A simple explanation",
    "examples": ["Long Long Long Example 1", "text text text Example 2"]
  }
  node = create_appropriate_node(sample_definition)
  assert isinstance(node, Definition)

  with pytest.raises(AttributeError): # because the correct attribute is intuitions (PLURAL FORM!)
    node.intuition == "A simple explanation"
  assert node.intuitions == ["A simple explanation"]
  with pytest.raises(AttributeError): # simply because the attribute doesn't exist
    node.proofs == ""
  with pytest.raises(ValueError):
    node.type = "Something Weird"

############################ DUNDERSCORE, WEIGHT TESTS ##########################################

def test_definition_dunderscore_exists_content():
  pre_node = {
    "name": "Triangle",
    "plural":"__Triangles__",
    "weight": 1,
    "def": "A __triangle__ is a 3 sided polygon.",
    "intuition": "A simple explanation",
    "examples": ["Long Long Long Example 1", "text text text Example 2"]
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Definition)

  with pytest.raises(AssertionError): # because a Definition's description MUST have dunderscores!
    node.description = "A triangle is a 3 sided polygon."
  with pytest.raises(AssertionError): # because we will automatically add the dunderscores to the names (of definitions) on the fly (this will be an optional setting for users, since some would not prefer the clutter of the underlines in the DAG itself
    node.name = "__DunderScore__"
  with pytest.raises(AssertionError): # because this *should* have dunderscores
    node.plural = "Triangles"

def test_theorem_no_dunderscore():
  pre_node = {
    "name": "Pythagorean theorem",
    "type": "thm",
    "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.",
    "intuition": "A simple explanation.",
    "examples": ["Example 1 is now long enough.", "Example 2 is now long."],
    "proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}
  }
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Theorem)

  with pytest.raises(AssertionError): # because a theorem cannot have dunderscores
    node.description = "A __triangle__ is a 3 sided polygon."
  with pytest.raises(AssertionError): # again, because a name should not have dunderscore (but we may add them on the fly)
    node.name = "__DunderScore__"

def test_exercise_no_dunderscore():
  pre_node={ "weight": 2, "exercise": "Three Four Five Triangle", "intuition": "Long enough 3^2+4^2=5^2", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Exercise)

  with pytest.raises(AssertionError): # exercises should NOT have dunderscores, anywhere
    node.description = "A __triangle__ is a 3 sided polygon."
  with pytest.raises(AssertionError):
    node.examples = ["__DunderScore__ is in here", "In here as __well__", "Will this pass?"]

def test_definition_weights():
  pre_node = {"name": "Triangle", "weight": 1, "def": "A __triangle__ is a 3 sided polygon.", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Definition)

  with pytest.raises(Exception): # we are no longer using the term "weight"
    node.weight = 5
  with pytest.raises(AssertionError): # importance can't be more than 10!
    node.importance = 100

def test_theorem_weights():
  pre_node = {"name": "Pythagorean theorem", "weight": 6, "thm": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Theorem)

  with pytest.raises(AssertionError): # importance must be at least 3!
    node.importance = 2

def test_exercise_weights():
  pre_node={ "weight": 2, "exercise": "Three Four Five Triangle", "intuition": "Long enough 3^2+4^2=5^2", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
  node = create_appropriate_node(pre_node)
  assert isinstance(node, Exercise)

  with pytest.raises(AssertionError): # importance must be 3 or less
    node.importance = 6

