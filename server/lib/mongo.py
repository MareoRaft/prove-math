import pymongo
# from passlib.context import CryptContext


class Mongo:


    def __init__(self, database, collection):
        self.address = pymongo.MongoClient("mongodb://localhost")
        self.database = database
        self.collection = collection

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
    def address(self,new_address):
        self._address=new_address

    @property
    def database(self):
        return self._database
    @database.setter
    def database(self, new_database):
        self._database=new_database

    @property
    def collection(self):
        return self._collection
    @collection.setter
    def collection(self, new_collection):
        self._collection=new_collection

    def insert_single(self, dic):
        self.address[self.database][self.collection].insert_one(dic)

    def insert_list(self, list_of_dicts):
        # Will complain if you attempt to insert duplicates
        self.address[self.database][self.collection].insert_many(list_of_dicts)

    def query(self, dict_fields=None):
        results = self.address[self.database][self.collection].find(dict_fields)

    def delete(self,dict_fields):
	# This will delete from all fields which match the parameter!!
        try:
            results= self.address[self.database][self.collection].delete_many(dict_fields)
            print("Number deleted: "+str(results.deleted_count))
        except Exception as e:
            print("Unexpected error:")


#Handles interactions with "users" Collection, Database
# class Users(Mongo):


#     def __init__(self):
#         Mongo(self,"provemath","users")
#         self.pass_hash = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

#     def make_pw_hash(self,pw):
#         crypt=self.pass_hash
#         return crypt.encrypt(pw)

#     def add_user(self, username,password, email):
#         password_hash=self.make_pw_hash(password)
#         user={'_id':username, 'password':password_hash,'email':email }

#         try:
#             self.address[self.database][self.collection].insert(user)

#         except pymongo.errors.OperationFailure:
#             print("Mongo Error")
#             return False

#         except pymongo.errors.DuplicateKeyError as e:
#             print ("Username is already taken")
#             return False

#         return True

#     def validate_login(self,username, password):
#         query={'_id':username}
#         crypt=self.pass_hash
#         user=None

#         try:
#             user=self.address[self.database][self.collection].find_one(query)
#         except:
#             print("Unexpected Error")

#         if user is None:
#             print("User or password not correct")
#             return None

#         if not crypt.verify(password,user['password']):
#             print("User or password not correct")
#             return None

#         return user

