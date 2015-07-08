from mongo import Mongo
import pytest
import sys

def test_Mongo_init():
    a=Mongo("test","people")
    assert a.database=="test"
    assert a.collection=="people"
    print(a)

def test_property_setter():
    a=Mongo("test","people")
    a.database="new_test"
    a.collection="new_collection"
    assert a.database=="new_test"
    assert a.collection=="new_collection"

def test_Mongo_equality():
    a=Mongo("test","people")
    b=Mongo("test","people")
    assert a==b

def test_Mongo_insert_then_query():
    #Mongodb must be running in background for this to work
    a=Mongo("test","people")
    dic = {"name": "Prof L", "company": "Rutgers", "interests": "Statistics"}
    a.insert_single(dic)
    results=a.query({"_name": "Prof L"})
    for x in results:
        assert dic==x

def test_Mongo_insert_then_delete():
    #Mongodb must be running in background for this to work
    a=Mongo("test","people")
    dic = {"name": "Prof I", "company": "Rutgers", "interests": "Statistics"}
    a.insert_single(dic)
    a.delete({"name":"Prof I"})
    results=a.query({"name":"Prof I"})
    assert results.count()==0

def test_Mongo_list_insert_then_query():
    #Mongodb must be running in background for this to work
    a=Mongo("test","people")
    dic1 = {"name": "Prof X", "company": "XMen", "interests": "Genetics"}
    dic2 = {"name": "Rufus", "company": "Unemployed", "interests": "food"}
    x=[dic1,dic2]
    a.insert_list(x)
    results1=a.query({"name":"Prof X"})
    for x in results1:
        assert dic1==x
    results1=a.query({"name":"Rufus"})
    for x in results1:
        assert dic2==x
    


"""
def test_...

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

"""
