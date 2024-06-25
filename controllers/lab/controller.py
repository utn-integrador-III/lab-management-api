from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.lab.model import LabModel
from controllers.lab.parser import query_parser_save
import logging


class LabController(Resource):
    route = "/lab"

    """
    Get all labs
    """
    def get(self):
        try:
            labs = LabModel.get_all()


            return ServerResponse(data=labs, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new Lab 
    """
    def post(self):
        try:
            lab=()
            
            return ServerResponse(lab.to_dict(), message="Lab successfully created", 
                                  message_code=LAB_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


    def put(self):
        try:
            updated_lab = None


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
    