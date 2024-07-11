from distutils import errors
from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class

from models.lab.db_queries import __dbmanager__
import logging
from .db_queries import Connection 

class LabModel:

    __dbmanager__ = Connection("lab_book")

    def __init__(self, lab_name=None, lab_num=None, _id=None, computers=None):
        self.lab_name = lab_name
        self.lab_num = lab_num
        self._id = _id
        self.computers=computers

    def to_dict(self):
        return {
            "lab_name": self.lab_name,
            "lab_num": self.lab_num,
            "computers": self.computers
        }

    # @classmethod
    def get_all():
        info_db = []
        response = __dbmanager__.get_all_data()

        for info in response:
            try:
                info_db.append(info)
            except Exception as ex:
                raise Exception(ex)

        return info_db

    @classmethod
    def get_by_lab_num(cls, lab_num):
        return None
    

    @classmethod
    def get_by_name(cls, lab_name):
        try:
            # Search for the lab by name in the database
            result = __dbmanager__.find_one({"lab_name": lab_name})
            if result:
                return cls(_id=result.get("_id"), lab_name=result.get("lab_name"))
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get zone by lab_name: " + str(ex))

    @classmethod
    def create(cls, data):
        try:
            labs = cls(**data)
            __dbmanager__.create_data(labs.to_dict())  # Insert data as a dictionary
            return labs
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create lab: " + str(ex))

        

    @classmethod
    def delete(cls, _id):
        try:
            result = __dbmanager__.delete_data(_id)
            if result:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, id):
        try:
            logging.info(f"Attempting to get lab book with id: {id}")
            if not ObjectId.is_valid(id):
                logging.warning(f"Invalid ObjectId: {id}")
                raise InvalidId(f"Invalid ObjectId: {id}")
            result = cls.__dbmanager__.get_by_id(id)
            logging.info(f"Result of get_by_id: {result}")
            return result
        except InvalidId as ex:
            logging.error(f"InvalidId error: {ex}")
            raise ex
        except Exception as ex:
            logging.error(f"Unexpected error in get_by_id: {ex}", exc_info=True)
            raise Exception(f"Error fetching lab by id {id}: {ex}")

        
    
    @classmethod
    def update(cls, lab_book_id, update_data):
        try:
            logging.info(f"Attempting to update lab book with id: {lab_book_id}")
            logging.info(f"Update data: {update_data}")
            result = cls.__dbmanager__.update_data(lab_book_id, update_data)
            logging.info(f"Update result: {result}")
            return result
        except Exception as ex:
            logging.error(f"Error updating lab book: {ex}", exc_info=True)
            return False


