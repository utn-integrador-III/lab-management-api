from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import INVALID_ID, NO_DATA, OK_MSG
from models.issue.model import IssueModel
from utils.auth_manager import auth_required
import logging
from bson.errors import InvalidId
from datetime import datetime

class IssueByIdController(Resource):
    route = "/issue/<string:id>"

    """
    Get issue by id
    """
    @auth_required(permission='read')
    def get(self, id, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            issue = IssueModel.get_by_id(id)
            if issue:
                # Convert ObjectId and datetime to string
                issue["_id"] = str(issue["_id"])
                if isinstance(issue["date_issue"], datetime):
                    issue["date_issue"] = issue["date_issue"].isoformat()
                for update_item in issue.get("update", []):
                    if isinstance(update_item, dict) and isinstance(update_item.get("date"), datetime):
                        update_item["date"] = update_item["date"].isoformat()

                return ServerResponse(
                    data=issue,
                    message="Successfully requested",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Issue does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data={},
                message="Invalid ID",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.error(f"Error getting issue by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)