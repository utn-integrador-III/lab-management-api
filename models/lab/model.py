from distutils import errors
from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class

from models.lab.db_queries import __dbmanager__
import logging


class LabModel:

    def __init__(self, lab_name=None, lab_num=None, _id=None, computers=None):
        self.lab_name = lab_name
        self.lab_num = lab_num
        self._id = _id
        self.computers = computers

    def to_dict(self):
        return {
            "lab_name": self.lab_name,
            "lab_num": self.lab_num,
            "computers": self.computers,
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
            # Ensure the id is a valid ObjectId
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")
            return __dbmanager__.get_by_id(id)
        except InvalidId as ex:
            raise ex  # Re-raise InvalidId to handle it specifically in the get method
        except Exception as ex:
            raise Exception(f"Error fetching zone by id {id}: {ex}")

    @classmethod
    def update(cls, id, update_data):
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid id value")

        id = ObjectId(id)
        result = __dbmanager__.update_data(id, update_data)
        if result:
            updated_zone = cls.get_by_id(str(id))
            return updated_zone
        else:
            return None
        
    @classmethod
    def get_by_num(cls, lab_num):
        try:
            result = __dbmanager__.find_one({"lab_num": lab_num})
            if result:
                return cls(_id=result.get("_id"), lab_name=result.get("lab_name"), lab_num=result.get("lab_num"))
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get lab by lab_num: " + str(ex))
