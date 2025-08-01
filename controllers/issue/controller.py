from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import ISSUE_EMAIL_REQUIRED, ISSUE_ID_REQUIRED, ISSUE_LAB_REQUIRED, ISSUE_NOT_FOUND, ISSUE_PERSON_REQUIRED, ISSUE_REQUIRED, ISSUE_OBSERVATIONS_REQUIRED, ISSUE_SUCCESSFULLY_DELETED, ISSUE_UPDATE_REQUIRED, ISSUE_SUCCESSFULLY_CREATED, ISUE_STATUS_PENDING, NO_DATA,ISSUE_SUCCESSFULLY_UPDATED,ISSUE_UNAUTHORIZED_ACTION
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

        if not current_user:
            return ServerResponse(
                data={},
                message="Unauthorized",
                status=StatusCode.UNAUTHORIZED,
            )

        try:
            issues = IssueModel.get_all()

            # Verificamos si el modelo devolvió un error
            if isinstance(issues, dict) and "error" in issues:
                return ServerResponse(
                    data={},
                    message=issues["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not issues:
                return ServerResponse(
                    data=[],
                    message="No Issues found",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )
            
            # El modelo ya nos devuelve los datos formateados
            return ServerResponse(data=issues, status=StatusCode.OK)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(
                data={},
                message=f"An unexpected error occurred: {str(ex)}",
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )

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

    @auth_required(permission='write', with_args=True)
    def put(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")
            
        try:
            data = request.get_json()
            _id = data.get('_id')
            issue_data = data.get('issue', [])
            observations = data.get('observations')
            email_user = data.get('email')

            if not _id:
                return ServerResponse(message='ID is required', status=StatusCode.BAD_REQUEST, message_code=ISSUE_ID_REQUIRED)

            if not observations:
                return ServerResponse(message='Observations are required', status=StatusCode.BAD_REQUEST, message_code=ISSUE_OBSERVATIONS_REQUIRED)

            if not isinstance(issue_data, list) or not issue_data:
                return ServerResponse(message='Issue data is required and must be a non-empty array', status=StatusCode.BAD_REQUEST, message_code=ISSUE_REQUIRED)

            if not email_user:
                return ServerResponse(message='Email is required', status=StatusCode.BAD_REQUEST, message_code=ISSUE_EMAIL_REQUIRED)

            issue = IssueModel.find_by_id(_id)

            if not issue:
                return ServerResponse(message='Issue not found', status=StatusCode.NOT_FOUND)

            if issue['status'] != 'Pending':
                return ServerResponse(message='Issue status must be Pending', status=StatusCode.BAD_REQUEST, message_code=ISUE_STATUS_PENDING)

            if issue.get("person", {}).get("email") != email_user:
                return ServerResponse(message='Unauthorized action', status=StatusCode.UNAUTHORIZED, message_code=ISSUE_UNAUTHORIZED_ACTION)

            # Update observations
            issue["observations"] = observations

            for item in issue_data:
                if not item.get('computer') or not item.get('description'):
                    return ServerResponse(message='Both computer and description are required and cannot be empty', status=StatusCode.BAD_REQUEST, message_code=ISSUE_REQUIRED)
                item['is_repaired'] = False

            issue["issue"] = issue_data

            # Convert datetime fields to strings
            if isinstance(issue.get("date_issue"), datetime):
                issue["date_issue"] = issue["date_issue"].isoformat()
            
            for update_item in issue.get("update", []):
                if isinstance(update_item.get("date"), datetime):
                    update_item["date"] = update_item["date"].isoformat()

            result = IssueModel.update_data(_id, issue)
            if not result:
                return ServerResponse(
                    message='Failed to update issue: No changes were made.',
                    status=StatusCode.BAD_REQUEST
                )
            issue['_id'] = str(issue['_id'])
            return ServerResponse(data=issue, message="Issue successfully updated", status=StatusCode.OK, message_code=ISSUE_SUCCESSFULLY_UPDATED)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


