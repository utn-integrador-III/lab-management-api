from datetime import datetime
from bson import ObjectId
from flask import request
from flask_restful import Resource
from utils.auth_manager import auth_required
from utils.message_codes import INVALID_ID, NO_DATA, OK_MSG
from utils.server_response import ServerResponse, StatusCode
from bson.errors import InvalidId
from models.booking.db_queries import __dbmanager__
import logging
from models.booking.model import BookingModel

def convert_to_serializable(data):
    """Convierte ObjectId y datetime a tipos serializables."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, list):
                data[key] = [convert_to_serializable(item) for item in value]
    elif isinstance(data, list):
        data = [convert_to_serializable(item) for item in data]
    return data

class BookingByIdController(Resource):
    route = "/booking/<string:id>"

    """
    Get booking by id
    """
    @auth_required(permission='read', with_args=True)
    def get(self, id):
        current_user = request.args.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")
        
        try:
            result = BookingModel.get_by_id(id)
            if result:
                result = convert_to_serializable(result)  # Convierte los datos aquí
                return ServerResponse(
                    data=result,
                    message="Booking found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Booking does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data={},
                message="Invalid booking ID",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.error(f"Error getting booking by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)