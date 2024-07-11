from distutils import errors
from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class

from models.lab.db_queries import __dbmanager__
import logging


class LabModel:

    def __init__(self, name=None, lab_num=None, _id=None, computers=None):
        self.name = name
        self.lab_num = lab_num
        self._id = _id
        self.computers = computers

    def to_dict(self):
        return {
            "lab_name": self.name,
            "lab_num": self.lab_num,
            "computers": self.computers,
        }

    # @classmethod
    def get_all():
        return []

    @classmethod
    def get_by_lab_num(cls, lab_num):
        return None

    @classmethod
    def create(cls, data):
        return None

    @classmethod
    def delete(cls, id):
        return None

    @classmethod
    def get_by_id(cls, id):
        return None

    @classmethod
    def update(cls, id, update_data):
        return None
