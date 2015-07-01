import pymongo
from passlib.context import CryptContext

class Mongo:
    def __init__(self,database,collection):
        self.address=pymongo.MongoClient("mongodb://localhost")
        self.database=database
        self.collection=collection
 
    def __repr__(self):
        msg="(add: %s, db: %s, collection: %s)\n " %(self.address, self.database, self.collection)
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

    def single_insert_to_mongo(self,dic):

        try:
            self.address[self.database][self.collection].insert_one(dic)
        except Exception as e:
            print("Unexpected error:")

    def list_insert_to_mongo(self,list_of_dicts):
        # Will complain if you attempt to insert duplicates
        try:
            self.address[self.database][self.collection].insert_many(list_of_dicts)
        except Exception as e:
            print("Unexpected error in list insert:"+str(type(e))+str(e))

    def query_mongo(self,dict_fields):
        try:
	#Results will be returned as json
            results= self.address[self.database][self.collection].find(dict_fields)
            for x in results:
                print(x)
        except Exception as e:
            print("Unexpected error in query:")

    def delete_from_mongo(self,dict_fields):
	# This will delete from all fields which match the parameter!!
        try:
            results= self.address[self.database][self.collection].delete_many(dict_fields)
            print("Number deleted: "+str(results.deleted_count))		
        except Exception as e:
            print("Unexpected error:")
#Handles interactions with User Collection, Database  
class Users(Mongo):
    def __init__(self):
        Mongo.__init__(self,"provemath","users")
        self.pass_hash=CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])
    def make_pw_hash(self,pw):
        crypt=self.pass_hash
        return crypt.encrypt(pw)

    def add_user(self, username,password, email):
        password_hash=self.make_pw_hash(password)
        user={'_id':username, 'password':password_hash,'email':email }
        
        try:
            self.address[self.database][self.collection].insert(user)
        
        except pymongo.errors.OperationFailure:
            print("Mongo Error")
            return False
        
        except pymongo.errors.DuplicateKeyError as e:
            print ("Username is already taken")
            return False

        return True

    def validate_login(self,username, password):
        query={'_id':username}
        crypt=self.pass_hash
        user=None

        try:
            user=self.address[self.database][self.collection].find_one(query)
        except:
            print("Unexpected Error")

        if user is None:
            print("User or password not correct")
            return None

        if not crypt.verify(password,user['password']):
            print("User or password not correct")
            return None

        return user
        


if __name__=="__main__":
    dic = {"name": "Prof K", "company": "Rutgers", "interests": "Statistics"}
    dic2= {"name": "JohnnyV", "company": "Dirtbikes INC", "interests": "Math Prof"}
    dic3= {"name": "Dino", "company":"Unemployed"}
    l=[dic2,dic3]

    a=Mongo("test","people")
    b=Users()
    b.add_user("Theodore","lala123","sampleEmail@gmail.com")
    print(b.validate_login("Theo","wrongpassword"))
    print(b.validate_login("Theo","lala123"))
    
    #print(a)
    #print(a.address)
    #a.single_insert_to_mongo(dic)
    #a.list_insert_to_mongo(l)
    #a.query_mongo({"_name":"vertex"})
    #a.delete_from_mongo({"name":"Prof K"})

