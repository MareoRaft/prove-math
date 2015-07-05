from mongo import Mongo

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

