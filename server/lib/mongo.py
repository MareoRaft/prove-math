import pymongo
# from passlib.context import CryptContext


class Mongo:


    def __init__(self, database, collection):
        self.address = pymongo.MongoClient("mongodb://localhost")
        self.database = database
        self.collection = collection
        # self.pass_hash = CryptContext(
        #     schemes=[
        #         "sha256_crypt",
        #         "md5_crypt",
        #         "des_crypt"])

    def __str__(self):
        msg = "(address: %s, db: %s, collection: %s)" % (self.address, self.database, self.collection)
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
        self.address[self.database][self.collection].insert_one(dic)

    def insert_many(self, list_of_dicts):
        # Will complain if you attempt to insert duplicates
        self.address[self.database][self.collection].insert_many(list_of_dicts)

    def update(self, query, update, options):
        self.address[self.database][self.collection].update(query, update, options)

    def find(self, dict_fields=None):
        return self.address[self.database][self.collection].find(dict_fields)

    def delete_many(self, dict_fields):
        # This will delete from all fields which match the parameter!!
        results = self.address[self.database][self.collection].delete_many(dict_fields)
        print("Number deleted: " + str(results.deleted_count))
