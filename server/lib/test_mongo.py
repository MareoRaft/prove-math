# system:
import pytest
import sys

# locals:
from lib.mongo import Mongo

def test_Mongo___init__():
    a = Mongo("test", "people")
    assert a.database == "test"
    assert a.collection == "people"

def test_property_setter():
    a = Mongo("test", "people")
    a.database = "new_test"
    a.collection = "new_collection"
    assert a.database == "new_test"
    assert a.collection == "new_collection"

def test_Mongo_equality():
    a = Mongo("test","people")
    b = Mongo("test","people")
    assert a == b

def test_Mongo_insert_then_find():
    #Mongodb must be running in background for this to work
    mongo = Mongo("test", "people")
    dic = {"name": "Darth Vader", "company": "Empire", "interests": "The Force"}
    mongo.insert_one(dic)
    results = mongo.find({"company": "Empire"})
    # raise Exception('type of results is '+str(type(results)))
    del dic['_id']
    for x in results:
        del x['_id']
        assert dic==x

def test_Mongo_insert_then_delete():
    #Mongodb must be running in background for this to work
    a = Mongo("test","people")
    dic = {"name": "Prof I", "company": "Rutgers", "interests": "Statistics"}
    a.insert_one(dic)
    a.delete_many({"name":"Prof I"})
    results = a.find({"name":"Prof I"})
    assert results.count() == 0

def test_Mongo_list_insert_then_find():
    #Mongodb must be running in background for this to work
    a = Mongo("test","people")
    dic1 = {"name": "Ethan Hunt", "company": "IMF", "interests": "Epionage"}
    dic2 = {"name": "Chef Eddie", "company": "Unemployed", "interests": "food"}
    x = [dic1,dic2]
    a.insert_many(x)
    results1 = a.find({"name":"Ethan Hunt"})
    del dic1['_id']
    del dic2['_id']
    for x in results1:
        del x["_id"]
        print(x)
        print(dic1)
        assert dic1 == x
    results1 = a.find({"name":"Chef Eddie"})
    for x in results1:
        print(x)
        print(dic2)
        del x["_id"]
        assert dic2 == x



"""
def test_...

    dic = {"name": "Prof K", "company": "Rutgers", "interests": "Statistics"}
    dic2 = {"name": "JohnnyV", "company": "Dirtbikes INC", "interests": "Math Prof"}
    dic3 = {"name": "Dino", "company":"Unemployed"}
    l = [dic2,dic3]

    a = Mongo("test","people")
    b = Users()
    b.add_user("Theodore","lala123","sampleEmail@gmail.com")
    print(b.validate_login("Theo","wrongpassword"))
    print(b.validate_login("Theo","lala123"))

    #print(a)
    #print(a.address)
    #a.single_insert_to_mongo(dic)
    #a.list_insert_to_mongo(l)
    #a.find_mongo({"_name":"vertex"})
    #a.delete_from_mongo({"name":"Prof K"})

"""
