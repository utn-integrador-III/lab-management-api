from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class

from models.issue.db_queries import __dbmanager__
import logging
from pymongo.errors import ServerSelectionTimeoutError

class IssueModel:

    def __init__(self, lab=None, date_issue=None, _id=None, person=None, issue=None, report_to=None, observations=None,
                 status=None, update=None):
        self.lab = lab
        self.date_issue = date_issue
        self._id = _id
        self.person=person
        self.issue = issue
        self.report_to=report_to
        self.observations = observations
        self.status = status
        self.update=update

    def to_dict(self):
        return {
            "lab": self.lab,
            "date_issue": self.date_issue,
            "person": self.person,
            "issue": self.issue,
            "report_to": self.report_to,
            "observations": self.observations,
            "status": self.status,
            "update": self.update
        }
    @classmethod
    def create(cls, data):
        try:
            issue = cls(**data)
            __dbmanager__.create_data(issue.to_dict()) 
            return issue
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create lab: " + str(ex))
        
    @classmethod
    def get_all(cls):
        try:
            info_db = []
            response = __dbmanager__.get_all_data()
            for info in response:
                info_db.append(info)
            return info_db
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(cls, _id):
        try:
            object_id = ObjectId(_id)
            issue = __dbmanager__.find_one({"_id": object_id})
            if issue:
                return issue
            return None
        except InvalidId:
            raise Exception("Invalid ID format")
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get issue by ID: " + str(ex))
        
    @classmethod
    def delete_if_pending(cls, _id):
        try:
            object_id = ObjectId(_id)
            issue = __dbmanager__.find_one({"_id": object_id})
            if issue and issue.get("status") == "Pending":
                __dbmanager__.delete_data(object_id)
                return True
            return False
        except InvalidId:
            raise Exception("Invalid ID format")
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to delete issue: " + str(ex))
    
    @staticmethod
    def find_by_id(lab_book_id):
        try:
            return __dbmanager__.get_by_id(lab_book_id)
        except ServerSelectionTimeoutError as e:
            logging.error(f"Database connection error: {e}")
            raise   
    
    @staticmethod
    def update(issue_id, data):
        try:
            result = __dbmanager__.update_data(issue_id, data)
            if not result:
                raise Exception("Failed to update issue: No changes were made.")
            return result
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update issue: " + str(ex))
        
    @classmethod    
    def update_data(cls,issue_id, data):
        try:
            result = __dbmanager__.update_data(issue_id, data)
            if not result:
                raise Exception("Failed to update issue: No changes were made.")
            return result
        except InvalidId:
            raise Exception("Invalid ID format")
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update issue: " + str(ex))

        