from db.mongo_client import Connection
from decouple import config
from bson.objectid import ObjectId

__dbmanager__ = Connection(config('LAB_BOOK_COLLECTION'))


#Metodos necesarios para la verificación de si existe el objeto
def find_by_id(lab_id):
    return __dbmanager__.collection.find_one({'_id': ObjectId(lab_id)})

def update(lab_id, update_data):
    return __dbmanager__.collection.update_one({'_id': ObjectId(lab_id)}, {'$set': update_data})
