import re
import subprocess

from lib.helper import json_import
from lib.node import create_appropriate_node
from lib.mongo import Mongo

collection = input('Which collection should we store the nodes in?: ')
db = Mongo("provemath", collection)

file_name = input('What is the name of the pre-json file?: ')
re.sub(r'^data/', '', file_name)
re.sub(r'\.pre-json$', '', file_name)
file_path = 'data/' + file_name + '.pre-json'
subprocess.check_output(['lib/pre-json_to_json.pl', file_path])

new_data_dictionary = json_import('data/' + file_name + '.json')

for pre_node in new_data_dictionary['nodes']:
    node = create_appropriate_node(pre_node)
    db.insert_one(node.__dict__)
