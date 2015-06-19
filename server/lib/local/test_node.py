import sys
from node import Node

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
            pass
