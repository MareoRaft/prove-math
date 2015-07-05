import re

import helper
from mongo import Mongo

collection = input('Which collection should we store the nodes in?: ')
db = Mongo("provemath", collection)

file_name = input('What is the name of the pre-json file?: ')
re.sub(r'^data/', '', file_name)
re.sub(r'\.pre-json$', '', file_name)
file_path = 'data/' + file_name + '.pre-json'
subprocess.check_output(['lib/pre-json-to-json.pl', file_path])

new_data_dictionary = helper.json_import('data/' + file_name + '.json')

for pre_node in new_data_dictionary['nodes']:
    node = Node(pre_node)
    db.single_insert( node.as_json )
