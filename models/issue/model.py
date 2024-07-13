from distutils import errors
from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class

from models.issue.db_queries import __dbmanager__
import logging


class IssueModel:

    def __init__(self, lab=None, date_issue=None, _id=None, person=None, issue=None, report_to=None, observations=None, notification_date=None,
                 status=None, update=None):
        self.lab = lab
        self.date_issue = date_issue
        self._id = _id
        self.person=person
        self.issue = issue
        self.report_to=report_to
        self.observations = observations
        self.notification_date=notification_date
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
            "notification_date": self.notification_date,
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
    def get_by_name(cls, lab):
        try:
            # Search for the lab by name in the database
            result = __dbmanager__.find_one({"lab": lab})
            if result:
                return cls(_id=result.get("_id"), lab=result.get("lab"))
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get zone by lab_name: " + str(ex))