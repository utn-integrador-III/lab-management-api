from flask_restful import Resource
from utils.server_response import *
from models.lab.model import LabModel
import logging
from bson.errors import InvalidId


class LabByIdController(Resource):

    route = "/lab/<string:id>"

    """
    Get lab by num
    """    
    def get(self,id):
        try:
            result = LabModel.get_by_id(id)
            if result:
                # Change to string the ObjectId
                result["_id"] = str(result["_id"]) if "_id" in result else None
                return ServerResponse(
                    data=result,
                    message="Zone found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Zone does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data={},
                message="Invalid zone ID",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.error(f"Error getting zone by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

 
        
   
    