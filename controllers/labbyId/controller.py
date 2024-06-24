from flask_restful import Resource
from utils.server_response import *
from models.lab.model import LabModel
import logging
from bson.errors import InvalidId


class LabByIdController(Resource):

    route = "/lab/<int:num>"

    """
    Get lab by num
    """    
    def get(self, num):
        try:
            result=None   
            return ServerResponse(
                data=result,
                message="Lab found",
                message_code=OK_MSG,
                status=StatusCode.OK,
            )
        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data={},
                message="Invalid lab num",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )
        except Exception as ex:
            logging.error(f"Error getting lab by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete a lab by num
    """
    def delete(self, num):
        try:            
            return ServerResponse(
                message="Lab successfully deleted",
                message_code=LAB_SUCCESSFULLY_DELETED,
                status=StatusCode.OK,
            )           
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
   
    