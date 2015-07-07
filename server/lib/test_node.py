import sys
import pytest
from node import Node

def test_theorem():
    pre_node = {"name": "Pythagorean theorem", "type": "theorem", "weight": 1, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."],"proof": {"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}}
    node = Node(pre_node)
    assert node.name=="Pythagorean theorem"
    assert node.type=="theorem"
    assert node.weight==1
    assert node.description=="When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2."
    assert node.examples== ["Example 1 is now long enough.", "Example 2 is now long."]
    assert node.proofs== [{"type": "fake", "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee."}] 
    with pytest.raises(AttributeError) as e:
        node.intuition=="A simple explanation"
    with pytest.raises(AttributeError) as e:
        node.plural==""
        



def test_stuff():
    sample_definition = {"name": "__Triangle__","plural":"__Triangles__", "type": "definition", "weight": 1, "description": "3 sided polygon", "intuition": "A simple explanation", "examples": ["Long Long Long Example 1", "text text text Example 2"]}
    node=Node(sample_definition)
    assert node.name=="__Triangle__"
    assert node.type=="definition"
    assert node.weight==1
    assert node.description=="3 sided polygon"
    assert node.plural=="__Triangles__"
    assert node.examples== ["Long Long Long Example 1", "text text text Example 2"]
    with pytest.raises(AttributeError) as e:
        node.intuition=="A simple explanation"
    with pytest.raises(AttributeError) as e:
         node.proofs==""




def test_node_copy():
     sample_theorem = {
     	"name": "Pythagorean theorem",
     	"type": "theorem",
     	"weight": 1,
     	"description": "a^2b^2=c^2",
     	"intuition": "A simple explanation",
     	"examples": ["Example 1", "Example 2"]
     }
     a = Node(sample_theorem)
     b = a.clone()
     assert id(a) != id(b)
     assert a==b
     pass

if __name__ == "__main__":
     test_theorem()


#     matt_example2=  {
#             "weight": 4,
#             "type": "exercise",
#             "content": "$ k \\binom nk = n \\binom{n-1}{k-1} $",
#            "proof": {
#                "type": "combinatorial",
#                "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee.",
#            },
#         }

#     thomas_example= {"definition":"If $E \subset S$, and $\exists \gamma \in S$ such that $\forall x \in E, x \geq \gamma$, then we say that $E$ is __bounded below__ by $\gamma"}

#     thomas_example_1={"definition":"If $E$ is __bounded gamma__ by $\gamma$, then we say that $\gamma$ is a __lower bound__ of $E$"}




# data_dictionary = helper.json_import('../../data/data-test.json')
# for x in data_dictionary['nodes']:
#   c = Node(x)
#     print(c)

