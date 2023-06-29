from celery import Celery
import pymongo

app = Celery("myapp", broker="pyamqp://guest@localhost//")

@app.task
def mongo_add(Supermarkt_name, json_list):
    client = pymongo.MongoClient("mongodb+srv://max916328:Mongodb_2020@cluster0.v24mw5y.mongodb.net/")
    db = client['Sortiment']
    db_collection = db[Supermarkt_name]
    db_collection.create_index([('name', pymongo.ASCENDING)], unique=True) 
    for item in json_list:    
            try:
                x = db_collection.insert_one(item)
                print(item["name"] + ": " + "Successfully added!")
            except pymongo.errors.DuplicateKeyError as error:
                # Ignore duplicates and continue with the next iteration
                print("ERROR: " + item["name"] + " was already added!")
                continue