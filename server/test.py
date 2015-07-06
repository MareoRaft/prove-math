from lib.local.node import Node

pre_node = {"name": "Pythagorean theorem", "type": "theorem", "weight": 1, "description": "When the leg is a and the leg is b and the hypotenuse is c, then a^2+b^2=c^2.", "intuition": "A simple explanation.", "examples": ["Example 1 is now long enough.", "Example 2 is now long."]}
node = Node(pre_node)
print(node.as_json())
