from pymongo import MongoClient
from decouple import config
from bson import ObjectId

# Conexión a MongoDB
client = MongoClient(config('MONGO_URL'))
db = client[config('MONGO_DB')]
__dbmanager__ = db[config('ISSUE_COLLECTION')]

def insert_data(data):
    return __dbmanager__.insert_one(data)

def get_all_data():
    return __dbmanager__.find()

def find_one(query):
    return __dbmanager__.find_one(query)

def delete_data(object_id):
    return __dbmanager__.delete_one({"_id": object_id})

def update_data(issue_id, data):
    return __dbmanager__.update_one({"_id": ObjectId(issue_id)}, {"$set": data})

def get_by_id(lab_book_id):
    return __dbmanager__.find_one({"_id": ObjectId(lab_book_id)})