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
    a = Mongo("test", "people")
    b = Mongo("test", "people")
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
    a = Mongo("test", "people")
    dic = {"name": "Prof I", "company": "Rutgers", "interests": "Statistics"}
    a.insert_one(dic)
    a.delete_many({"name":"Prof I"})
    results = a.find({"name":"Prof I"})
    assert results.count() == 0

def test_Mongo_list_insert_then_find():
    #Mongodb must be running in background for this to work
    a = Mongo("test", "people")
    dic1 = {"name": "Ethan Hunt", "company": "IMF", "interests": "Epionage"}
    dic2 = {"name": "Chef Eddie", "company": "Unemployed", "interests": "food"}
    x = [dic1,dic2]
    a.insert_many(x)
    results1 = a.find({"name":"Ethan Hunt"})
    del dic1['_id']
    del dic2['_id']
    for x in results1:
        del x["_id"]
        assert dic1 == x
    results1 = a.find({"name":"Chef Eddie"})
    for x in results1:
        del x["_id"]
        assert dic2 == x

def test_Mongo_find_one():
    a = Mongo("test", "people")
    dic = {"name": "Prof I", "company": "Rutgers", "interests": "Statistics"}
    a.insert_one(dic)
    result = a.find_one({"name": "Prof I"})
    assert result is not None

    a.delete_many({"name":"Prof I"})
    result = a.find_one({"name": "Prof I"})
    assert result is None

def test_Mongo_proposed_id_to_good_id():
    a = Mongo("test", "people")
    dic = {"_id": "takenid"}
    a.delete_many(dic)
    a.insert_one(dic)
    proposed_id = "takenid"
    assert a.proposed_id_to_good_id(proposed_id) == "takenid2"

    a.delete_many(dic)
    assert a.proposed_id_to_good_id(proposed_id) == "takenid"
    # the above ID is NO LONGER TAKEN

    a.insert_one(dic)
    a.insert_one({"_id": "takenid2"})
    assert a.proposed_id_to_good_id(proposed_id) == "takenid3"

