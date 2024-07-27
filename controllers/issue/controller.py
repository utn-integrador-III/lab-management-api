from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import ISSUE_LAB_REQUIRED, ISSUE_NOT_FOUND, ISSUE_PERSON_REQUIRED, ISSUE_REQUIRED, ISSUE_REPORT_TO_REQUIRED, ISSUE_OBSERVATIONS_REQUIRED, ISSUE_STATUS_REQUIRED, ISSUE_SUCCESSFULLY_DELETED, ISSUE_UPDATE_REQUIRED, LAB_ALREADY_EXIST, ISSUE_SUCCESSFULLY_CREATED, NO_DATA
from models.issue.model import IssueModel
from utils.auth_manager import auth_required
import logging
from datetime import datetime

class IssueController(Resource):
    route = "/issue"


    """
    Get all issue 
    """
    @auth_required(permission='read', with_args=True)
    def get(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            Issues = IssueModel.get_all()
            if isinstance(Issues, dict) and "error" in Issues:
                return ServerResponse(
                    data={},
                    message=Issues["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not Issues:
                return ServerResponse(
                    data={},
                    message="No Issues found",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )

            # Convert ObjectId and datetime to string
            for issue in Issues:
                issue["_id"] = str(issue["_id"])
                if isinstance(issue["date_issue"], datetime):
                    issue["date_issue"] = issue["date_issue"].isoformat()
                for update_item in issue.get("update", []):
                    if isinstance(update_item, dict) and isinstance(update_item.get("date"), datetime):
                        update_item["date"] = update_item["date"].isoformat()

            return ServerResponse(data=Issues, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new issue 
    """
    @auth_required(permission='write', with_args=True)
    def post(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            # Obtain data from the body of the request
            data = request.get_json()

            # Validate required field 'lab'.
            if not data.get("lab"):
                return ServerResponse(message='lab is required', 
                                      message_code=ISSUE_LAB_REQUIRED, status=StatusCode.BAD_REQUEST)


            # Validate required field 'person'.
            if not data.get("person"):
                return ServerResponse(message='person is required', 
                                      message_code=ISSUE_PERSON_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required sub-fields in 'person'
            person = data["person"]
            if not person.get("email"):
                return ServerResponse(message='email in person is required', 
                                      message_code=ISSUE_PERSON_REQUIRED, status=StatusCode.BAD_REQUEST)
            if not person.get("student_name"):
                return ServerResponse(message='student_name in person is required', 
                                      message_code=ISSUE_PERSON_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'issue'.
            if not data.get("issue"):
                return ServerResponse(message='issue is required', 
                                      message_code=ISSUE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate each issue item
            for issue_item in data["issue"]:
                if not issue_item.get("computer"):
                    return ServerResponse(message='computer in issue is required', 
                                          message_code=ISSUE_REQUIRED, status=StatusCode.BAD_REQUEST)
                if not issue_item.get("description"):
                    return ServerResponse(message='description in issue is required', 
                                          message_code=ISSUE_REQUIRED, status=StatusCode.BAD_REQUEST)
                # Set default value for 'is_repaired'
                if 'is_repaired' not in issue_item:
                    issue_item['is_repaired'] = False
                
            # Set default values for optional fields
            if 'report_to' not in data:
                data['report_to'] = ""
            if 'status' not in data:
                data['status'] = "Pending"
            if 'update' not in data:
                data['update'] = []
            
            # Add current date for 'date_issue' and 'notification_date'
            data["date_issue"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            # Validate required field 'observations'.
            if not data.get("observations"):
                return ServerResponse(message='observations is required', 
                                      message_code=ISSUE_OBSERVATIONS_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate that 'person' is a dictionary
            if not isinstance(data["person"], dict):
                return ServerResponse(message='person must be a dictionary', 
                                      message_code=ISSUE_PERSON_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Verify that 'issue' is an array and not empty
            if not isinstance(data["issue"], list) or len(data["issue"]) == 0:
                return ServerResponse(message='issue must be a non-empty array', 
                                      message_code=ISSUE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Verify that 'update' is an array (no longer needs to be non-empty)
            if not isinstance(data["update"], list):
                return ServerResponse(message='update must be an array', 
                                      message_code=ISSUE_UPDATE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Create and save the new laboratory issue
            lab_issue = IssueModel.create(data)
            return ServerResponse(lab_issue.to_dict(), message="Issue successfully created", 
                                  message_code=ISSUE_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete a issue 
    """
    @auth_required(permission='delete', with_args=True)
    def delete(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            data = request.get_json()
            _id = data.get('_id')

            if not _id:
                return ServerResponse(
                    message='ID is required',
                    status=StatusCode.BAD_REQUEST
                )

            deleted = IssueModel.delete_if_pending(_id)
            if deleted:
                return ServerResponse(
                    message='Issue successfully deleted',
                    message_code=ISSUE_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK
                )
            else:
                return ServerResponse(
                    message='Issue not found or status is not pending',
                    message_code=ISSUE_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
