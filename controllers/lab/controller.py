from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.lab.model import LabModel
from controllers.lab.parser import query_parser_save
from utils.auth_manager import auth_required
import logging
from bson.errors import InvalidId

class LabController(Resource):
    route = "/lab"

    """
    Get all labs
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
            labs = LabModel.get_all()

            if isinstance(labs, dict) and "error" in labs:
                return  ServerResponse(
                    data={},
                    message= labs["error"],
                    status= StatusCode.INTERNAL_SERVER_ERROR,
                )
            
            if not labs:  # If there are no lab
                return ServerResponse(
                    data={},
                    message="No labs found",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )

            # Convert ObjectId to string
            for lab in labs:
                lab["_id"] = str(lab["_id"])

            return ServerResponse(data=labs, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new Lab 
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

            # Validate required field 'lab_name'.
            if not data.get("lab_name"):
                return ServerResponse(message='lab_name is required', 
                                    message_code=LAB_NAME_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'lab_num'.
            if not data.get("lab_num"):
                return ServerResponse(message='lab_num is required', 
                                    message_code=LAB_NUM_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required field 'computers
            if not data.get("computers"):
                return ServerResponse(message='computers is required', 
                                    message_code=LAB_COMPUTERS_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Verify that 'computers' is an array and not empty
            if not isinstance(data["computers"], list) or len(data["computers"]) == 0:
                return ServerResponse(message='computers must be a non-empty array', 
                                    message_code=LAB_COMPUTERS_REQUIRED, status=StatusCode.BAD_REQUEST)


            # Validate if the laboratory already exists by num
            lab_exists = LabModel.get_by_num(data.get("lab_num"))
            if lab_exists:
                return ServerResponse(message='lab_num already exists', 
                                    message_code=LAB_ALREADY_EXIST, status=StatusCode.CONFLICT)

            # Create and save the new laboratory
            labs = LabModel.create(data)
            return ServerResponse(labs.to_dict(), message="lab successfully created", 
                                message_code=LAB_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
    @auth_required(permission='update', with_args=True)
    def put(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            # Get update data from the request body
            update_data = request.get_json()

            # Validate if valid update data was provided
            if not update_data or not isinstance(update_data, dict) or len(update_data) == 0:
                return ServerResponse(
                    message="No valid data provided for update",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Extract ID from update data and ensure it's present
            id = update_data.get("_id")
            if not id:
                return ServerResponse(
                    message="ID is required in the update data",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Remove ID from update data to prevent updating the ID
            update_data.pop("_id", None)

            # Validate additional fields not allowed
            allowed_fields = {"lab_name", "lab_num", "computers"}  # Define the allowed fields
            additional_fields = set(update_data.keys()) - allowed_fields
            if additional_fields:
                return ServerResponse(
                    message=f"Additional fields not allowed: {', '.join(additional_fields)}",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Check if the labs exists by ID
            lab = LabModel.get_by_id(id)
            if not lab:
                return ServerResponse(
                    message="lab does not exist",
                    message_code=LAB_NOT_FOUND,
                    status=StatusCode.BAD_REQUEST
                )

            # Update labs
            updated_lab = LabModel.update(id, update_data)
            if not updated_lab:
                return ServerResponse(
                    message="An error occurred while updating the lab",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            # Convert ObjectId to string if it exists in the updated labs
            updated_lab["_id"] = str(updated_lab["_id"]) if "_id" in updated_lab else None

            # Successful response
            return ServerResponse(
                data=updated_lab,
                message="Lab successfully updated",
                message_code=LAB_SUCCESSFULLY_UPDATED,
                status=StatusCode.OK,
            )

        except ValueError as ex:
            # Invalid ID handling
            logging.error(f"Invalid ID: {ex}")
            return ServerResponse(
                message="Invalid ID format",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            # General exception handling
            logging.error(f"Unexpected error: {ex}")
            return ServerResponse(
                message="An error occurred while updating the lab",
                message_code=INTERNAL_SERVER_ERROR_MSG,
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )
        
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
            update_data = request.get_json()
            update_data = update_data.get("_id")
            result = LabModel.delete(update_data)
            if result:
                return ServerResponse(
                    message="lab successfully deleted",
                    message_code=LAB_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="The lab no exists and cannot be deleted.",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        