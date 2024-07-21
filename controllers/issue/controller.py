from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import ISSUE_LAB_REQUIRED, ISSUE_PERSON_REQUIRED, ISSUE_REQUIRED, ISSUE_REPORT_TO_REQUIRED, ISSUE_OBSERVATIONS_REQUIRED, ISSUE_STATUS_REQUIRED, ISSUE_UPDATE_REQUIRED, LAB_ALREADY_EXIST, ISSUE_SUCCESSFULLY_CREATED
from models.issue.model import IssueModel
from utils.auth_manager import auth_required
import logging
from datetime import datetime

class IssueController(Resource):
    route = "/issue"

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

            # Add current date for 'date_issue' and 'notification_date'
            data["date_issue"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            data["notification_date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

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
                
                if "is_repaired" not in issue_item or not isinstance(issue_item["is_repaired"], bool):
                    return ServerResponse(message='is_repaired in issue must be a boolean', 
                                          message_code=ISSUE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'report_to'.
            if not data.get("report_to"):
                return ServerResponse(message='report_to is required', 
                                      message_code=ISSUE_REPORT_TO_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'observations'.
            if not data.get("observations"):
                return ServerResponse(message='observations is required', 
                                      message_code=ISSUE_OBSERVATIONS_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'status'.
            if not data.get("status"):
                return ServerResponse(message='status is required', 
                                      message_code=ISSUE_STATUS_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'update'.
            if not data.get("update"):
                return ServerResponse(message='update is required', 
                                      message_code=ISSUE_UPDATE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate that 'person' is a dictionary
            if not isinstance(data["person"], dict):
                return ServerResponse(message='person must be a dictionary', 
                                      message_code=ISSUE_PERSON_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Verify that 'issue' is an array and not empty
            if not isinstance(data["issue"], list) or len(data["issue"]) == 0:
                return ServerResponse(message='issue must be a non-empty array', 
                                      message_code=ISSUE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Verify that 'update' is an array and not empty
            if not isinstance(data["update"], list) or len(data["update"]) == 0:
                return ServerResponse(message='update must be a non-empty array', 
                                      message_code=ISSUE_UPDATE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate that each item in 'update' has 'observation'
            for update_item in data["update"]:
                if not update_item.get("observation"):
                    return ServerResponse(message='Each update item must have an observation', 
                                          message_code=ISSUE_UPDATE_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Add current date for 'update' items if not provided
            for update_item in data["update"]:
                if not update_item.get("date"):
                    update_item["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            # Validate if the laboratory already exists by ID
            labs_exists = IssueModel.get_by_name(data.get("lab"))
            if labs_exists:
                return ServerResponse(message='Issue already exists', 
                                      message_code=LAB_ALREADY_EXIST, status=StatusCode.CONFLICT)

            # Create and save the new laboratory issue
            lab_issue = IssueModel.create(data)
            return ServerResponse(lab_issue.to_dict(), message="Issue successfully created", 
                                  message_code=ISSUE_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
