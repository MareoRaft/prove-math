import sys
import pytest
from lib.node import Theorem
from lib.node import Exercise
from lib.node import Definition

sample_theorem = {
     	"name": "Pythagorean theorem",
     	"weight": 8,
     	"description": "a^2b^2=c^2",
     	"intuition": "A simple explanation",
     	"examples": ["Example 1", "Example 2"]
     }


##########################INIT, SETTERS/GETTERS, ATTRIBUTE TESTS################

def test_theorem_copy():
     global sample_theorem
     a = Theorem(sample_theorem)
     b = a.clone()
     assert id(a) != id(b)
     assert a==b
     pass



def test_theorem_setter_getter():
    pre_node = {"name": "Pythagorean theorem", "weight": 6, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node = Theorem(pre_node)
    print(node)
    assert node.name=="Pythagorean theorem"
    assert node.type=="theorem"
    assert node.weight==6
    assert node.description=="When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2."
    assert node.intuitions==["A simple explanation."]
    assert node.examples== ["Example 1 is now long enough.", "Example 2 is now long."]
    assert node.proofs== [{"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}]

def test_theorem_bad_attributes():
    pre_node = {"name": "Pythagorean theorem", "weight": 6, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node = Theorem(pre_node)
    with pytest.raises(AttributeError) as e:
        node.intuition=="A simple explanation"
    with pytest.raises(AttributeError) as e:
        node.plural==""

def test_exercise_setter_getter():
      pre_node = { "weight": 2, "description": "Three Four Five Triangle", "intuition": "3^2+4^2=5^2", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
      node=Exercise(pre_node)
      print(node)
      assert node.name==None
      assert node.type=="exercise"
      assert node.weight==2
      assert node.description=="Three Four Five Triangle"



def test_exercise_bad_attributes():
          pre_node = { "weight": 2, "description": "Three Four Five Triangle", "intuition": "3^2+4^2=5^2", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
          node=Exercise(pre_node)
          with pytest.raises(AttributeError) as e:
              node.plural==""
          
          
def test_definition_setters_getters():
    sample_definition = {"name": "Triangle", "weight": 1, "description": "A __triangle__ is a 3 sided polygon.", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
    node=Definition(sample_definition)
    print(node)
    assert node.name=="Triangle"
    assert node.type=="definition"
    assert node.weight==1
    assert node.description=="A __triangle__ is a 3 sided polygon."
    #assert node.plural=="__Triangles__"
    assert node.examples== ["Long Long Long Example 1", "text text text Example 2"]


def test_definition_bad_attributes():
    sample_definition = {"name": "Triangle", "weight": 1, "description": "A __triangle__ is a 3 sided polygon.", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
    node=Definition(sample_definition)
    with pytest.raises(AttributeError) as e:
        node.intuition=="A simple explanation"
    with pytest.raises(AttributeError) as e:
        node.proofs==""
    with pytest.raises(ValueError) as e:
        node.type="Something Weird"

############################ DUNDERSCORE, WEIGHT TESTS ##########################################

def test_definition_dunderscore_exists_content():
    sample_definition = {"name": "Triangle","plural":"__Triangles__", "weight": 1, "description": "A __triangle__ is a 3 sided polygon.", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
    node=Definition(sample_definition)
    with pytest.raises(AssertionError) as e:
        node.description="A triangle is a 3 sided polygon."
    with pytest.raises(AssertionError) as e:
        node.name="__DunderScore__"
    with pytest.raises(AssertionError) as e:
        node.plural="Triangles"

def test_theorem_no_dunderscore():
    pre_node = {"name": "Pythagorean theorem", "weight": 6, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node = Theorem(pre_node)
    with pytest.raises(AssertionError) as e:
        node.description="A __triangle__ is a 3 sided polygon."
    with pytest.raises(AssertionError) as e:
        node.name="__DunderScore__"

def test_exercise_no_dunderscore():
    pre_node={ "weight": 2, "description": "Three Four Five Triangle", "intuition": "3^2+4^2=5^2", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node=Exercise(pre_node)
    with pytest.raises(AssertionError) as e:
        node.description="A __triangle__ is a 3 sided polygon."
    with pytest.raises(AssertionError) as e:
        node.examples=["__DunderScore__ is in here", "In here as __well__", "Will this pass?"]

def test_definition_weights():
    sample_definition = {"name": "Triangle", "weight": 1, "description": "A __triangle__ is a 3 sided polygon.", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
    node=Definition(sample_definition)
    with pytest.raises(AssertionError) as e:
        node.weight=100

def test_theorem_weights():
     pre_node = {"name": "Pythagorean theorem", "weight": 6, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
     node = Theorem(pre_node)
     with pytest.raises(AssertionError) as e:
         node.weight=2
    

def test_exercise_weights():
    pre_node={ "weight": 2, "description": "Three Four Five Triangle", "intuition": "3^2+4^2=5^2", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node=Exercise(pre_node)
    with pytest.raises(AssertionError) as e:
         node.weight=6
    
    



