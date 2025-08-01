from bson import ObjectId
from bson.errors import InvalidId 
from models.issue.db_queries import __dbmanager__
import logging
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime

class IssueModel:

    def __init__(self, lab=None, date_issue=None, _id=None, person=None, issue=None, report_to=None, observations=None,
                 status=None, update=None):
        self.lab = lab
        self.date_issue = date_issue
        self._id = _id
        self.person = person
        self.issue = issue
        self.report_to = report_to
        self.observations = observations
        self.status = status
        self.update = update

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
            issue_data = issue.to_dict()
            result = __dbmanager__.insert_one(issue_data)
            if result.inserted_id:
                issue._id = str(result.inserted_id) 
                return issue  
            raise Exception("Failed to create issue")
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create issue: " + str(ex))

    @classmethod
    def _format_issue_data(cls, issues):
        formatted_issues = []
        for issue in issues:
            if isinstance(issue, dict):
                if "_id" in issue:
                    issue["_id"] = str(issue["_id"])
                
                if "date_issue" in issue and isinstance(issue["date_issue"], datetime):
                    issue["date_issue"] = issue["date_issue"].isoformat()
                
                for update_item in issue.get("update", []):
                    if isinstance(update_item, dict) and isinstance(update_item.get("date"), datetime):
                        update_item["date"] = update_item["date"].isoformat()
                
                formatted_issues.append(issue)
        return formatted_issues

    @classmethod
    def get_all(cls):
        try:
            issues_from_db = list(__dbmanager__.find()) 
            return cls._format_issue_data(issues_from_db)
        except Exception as ex:
            logging.exception(ex)
            return {"error": str(ex)}
        
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
                __dbmanager__.delete_one({"_id": object_id}) 
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
            return __dbmanager__.find_one({"_id": ObjectId(lab_book_id)})  
        except ServerSelectionTimeoutError as e:
            logging.error(f"Database connection error: {e}")
            raise  
    
    @staticmethod
    def update(issue_id, data):
        try:
            result = __dbmanager__.update_one({"_id": ObjectId(issue_id)}, {"$set": data}) 
            if result.modified_count > 0:
                return result
            raise Exception("Failed to update issue: No changes were made.")
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update issue: " + str(ex))
        
    @classmethod     
    def update_data(cls, issue_id, data):
        try:
            result = __dbmanager__.update_one({"_id": ObjectId(issue_id)}, {"$set": data}) 
            if result.modified_count > 0:
                return result
            raise Exception("Failed to update issue: No changes were made.")
        except InvalidId:
            raise Exception("Invalid ID format")
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update issue: " + str(ex))