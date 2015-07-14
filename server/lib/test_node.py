import sys
import pytest
from lib.node import Theorem
from lib.node import Exercise
from lib.node import Definition

# Leave out the type since we plan to check it on the outside
def test_theorem_copy():
     sample_theorem = {
     	"name": "Pythagorean theorem",
     	"weight": 8,
     	"description": "a^2b^2=c^2",
     	"intuition": "A simple explanation",
     	"examples": ["Example 1", "Example 2"]
     }
     a = Theorem(sample_theorem)
     b = a.clone()
     assert id(a) != id(b)
     assert a==b
     pass


def test_theorem():
    pre_node = {"name": "Pythagorean theorem", "weight": 6, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node = Theorem(pre_node)
    print(node)
    assert node.name=="Pythagorean theorem"
    assert node.type=="theorem"
    assert node.weight==6
    assert node.description=="When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2."
    assert node.examples== ["Example 1 is now long enough.", "Example 2 is now long."]
    assert node.proofs== [{"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}]
    with pytest.raises(AttributeError) as e:
        node.intuition=="A simple explanation"
    with pytest.raises(AttributeError) as e:
        node.plural==""


def test_definition():
    sample_definition = {"name": "__Triangle__", "weight": 1, "description": "A __triangle__ is a 3 sided polygon.", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
    node=Definition(sample_definition)
    print(node)
    assert node.name=="__Triangle__"
    assert node.type=="definition"
    assert node.weight==1
    assert node.description=="A __triangle__ is a 3 sided polygon."
    #assert node.plural=="__Triangles__"
    assert node.examples== ["Long Long Long Example 1", "text text text Example 2"]
    with pytest.raises(AttributeError) as e:
        node.intuition=="A simple explanation"
    with pytest.raises(AttributeError) as e:
        node.proofs==""
    with pytest.raises(ValueError) as e:
        node.type="Something Weird"









