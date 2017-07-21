""" See api.mongodb.com/python/current/api/pymongo/collection.html for documentation """

# third party:
import pymongo

from lib.helper import increment_string_counter


class Mongo:


    def __init__(self, database, collection):
        self.address = pymongo.MongoClient('mongodb://localhost')
        self.database = database
        self.collection = collection

    def __str__(self):
        msg = '(address: {}, db: {}, collection: {})'.format(self.address, self.database, self.collection)
        return msg

    def __eq__(self, other):
        if self.database == other.database and self.collection == other.collection:
            return True
        else:
            return False

    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def database(self):
        return self._database
    @database.setter
    def database(self, new_database):
        self._database = new_database

    @property
    def collection(self):
        return self._collection
    @collection.setter
    def collection(self, new_collection):
        self._collection = new_collection

    def insert_one(self, dic):
        # complains if what you try to insert already exists???
        self.address[self.database][self.collection].insert_one(dic)

    def insert_many(self, list_of_dicts):
        # Will complain if you attempt to insert duplicates
        self.address[self.database][self.collection].insert_many(list_of_dicts)

    def replace_one(self, query, replacement, **options):
        self.address[self.database][self.collection].replace_one(query, replacement, **options)

    # deprecated.  use replace_one(), update_one(), or update_many() instead.
    def update(self, query, update, options):
        self.address[self.database][self.collection].update(query, update, options)

    def upsert(self, query, update):
        self.address[self.database][self.collection].update(query, update, upsert=True)

    def find_one(self, dict_fields=None, projection=None):
        return self.address[self.database][self.collection].find_one(dict_fields, projection)

    def find(self, dict_fields=None, projection=None):
        return self.address[self.database][self.collection].find(dict_fields, projection)

    def delete_one(self, dict_fields):
        results = self.address[self.database][self.collection].delete_one(dict_fields)

    def delete_many(self, dict_fields):
        # This will delete from all fields which match the parameter!!
        results = self.address[self.database][self.collection].delete_many(dict_fields)
        print("Number deleted: " + str(results.deleted_count))

    def proposed_id_to_good_id(self, proposed_id):
        while True:
            result = self.find_one({ "_id": proposed_id })
            if result is None:
                return proposed_id
            else:
                proposed_id = increment_string_counter(proposed_id)

