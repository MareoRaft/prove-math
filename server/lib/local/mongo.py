import pymongo


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


if __name__=="__main__":
    dic = {"name": "Prof K", "company": "Rutgers", "interests": "Statistics"}
    dic2= {"name": "JohnnyV", "company": "Dirtbikes INC", "interests": "Math Prof"}
    dic3= {"name": "Dino", "company":"Unemployed"}
    l=[dic2,dic3]

    a=Mongo("test","people")
    print(a)
    print(a.address)
    a.single_insert_to_mongo(dic)
    a.list_insert_to_mongo(l)
    a.query_mongo({"_name":"vertex"})
    a.delete_from_mongo({"name":"Prof K"})

