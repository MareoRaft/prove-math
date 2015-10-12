import mongo


class User:


    USERS = mongo.Mongo("provemath", "users")

    def __init__(self, account_type, account_id):
        # if user exists, retrieve their dictionary
        self.dic = USERS.find('use account_type and account_id to retreive from Mongo')
        # otherwise, make a new dictionary and store it into the db
        if self.dic is some undefined thing:
            self.dic = _default_dic()
            USERS.insert_one('use acc_type and id again to set info in')

    def _default_dic():
        return {
            nodes: [],
            blabladefault things: '',
        }

        # here are the default things i have so far on the javascript side:
        # prefs: {
        #     display_name_capitalization: "title", // can be null, "sentence", or "title"
        #     underline_definitions: false, // can be true or false // do you want definitions to be underlined in the DAG view?
        #     show_description_on_hover: false, // can be true or false
        # },
        # learned_node_ids: [],


    def learn_node(self, node_json):
        node = Node(json.loads(node_json))
        USERS.insert_one(.....node) # or do we need upsert or append?
        # send info down to all other clients (if user is logged in on multiple computers)
        tornado.websockethandler.send_to_multiple_accounts({ command: 'learn-node', node: node })

    def unlearn_node(self, node_json):
        # same thing, but REMOVE node from database

    def set_pref(self, pref_json):
        # same thing, but replace current pref value in database with pref_json value
        # for example, pref_json could be { underline_definitions: true }

