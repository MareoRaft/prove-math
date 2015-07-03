import sys

from lib.local.node import Node

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

def test_Theorem___init__():
    sample_theorem = {"name": "Pythagorean theorem", "type": "theorem", "weight": 1, "description": "a^2+b^2=c^2", "intuition": "A simple explanation", "examples": ["Example 1", "Example 2"]}

def test_stuff():
    sample_definition = {"name": "triangle","plural":"triangles", "type": "definition", "weight": 1, "description": "3 sided polygon", "intuition": "A simple explanation", "examples": ["Example 1", "Example 2"]}
    matt_example1=  {
            "name": "Choosy Identity",
            "weight": 3,
            "thm": "$ \\binom nk = \\binom{n}{n-k} $",
            "proofs": [
                "Apply $\\binom nk = \\frac{n!}{k!(n-k)!} = \\frac{n!}{[n-(n-k)]!(n-k)!} = \\binom{n}{n-k} $",
                {
                    "type": "combinatorial",
                    "content": "Left side: We have $n$ puppies.  We choose $k$ of them and color them blue.  We color the rest of them red.  Right side: We have $n$ puppies.  We choose $n-k$ of them and color them red.  We color the rest of them blue.",
                },
            ],
        }

    matt_example2=  {
            "weight": 4,
            "type": "exercise",
            "content": "$ k \\binom nk = n \\binom{n-1}{k-1} $",
            "proof": {
                "type": "combinatorial",
                "content": "Left side: You have $n$ people.  You choose $k$ of them to be in a committee, and from the committee, you choose $1$ to be the chairperson.  Right side: You have $n$ people.  You choose $1$ of them to be the chairperson.  From the remaining $n-1$ of them, you choose $k-1$ of them to complete the committee.",
            },
        }

    thomas_example= {"definition":"If $E \subset S$, and $\exists \gamma \in S$ such that $\forall x \in E, x \geq \gamma$, then we say that $E$ is __bounded below__ by $\gamma"}

    thomas_example_1={"definition":"If $E$ is __bounded gamma__ by $\gamma$, then we say that $\gamma$ is a __lower bound__ of $E$"}



    #a = Node(sample_theorem) # incorporate this commented stuff into a test or delete it
    #b = Node(sample_definition)
    #c= Node(matt_example1)
    #d=Node(matt_example2)
    #e=Node(thomas_example)
    #f=Node(thomas_example_1)
    #print(a)
    #print(b)
    #print(c)
    #print(d.__dict__)
    #print(e.__dict__)
    #print(f.__dict__)
        #Importing the same documents from a file

    #data_dictionary = helper.json_import('../../data/data-test.json')
    #for x in data_dictionary['nodes']:
    #   c = Node(x)
        #print(c)
    a=Mongo("provemath", "combinatorics")

    new_data_dictionary = helper.json_import('../../data/combinatorics.json')
    for x in new_data_dictionary['nodes']:
        c=Node(x)
        #print(c.__dict__)
        a.single_insert_to_mongo(c.__dict__)

