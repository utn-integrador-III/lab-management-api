from flask_restful import Resource
from utils.server_response import *
from models.lab.model import LabModel
from utils.auth_manager import auth_required
import logging
from bson.errors import InvalidId


class LabByIdController(Resource):

    route = "/lab/<string:id>"

    """
    Get lab by num
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
            result = LabModel.get_by_id(id)
            if result:
                # Change to string the ObjectId
                result["_id"] = str(result["_id"]) if "_id" in result else None
                return ServerResponse(
                    data=result,
                    message="labs found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="labs does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data={},
                message="Invalid lab ID",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.error(f"Error getting lab by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

 
        
   
    