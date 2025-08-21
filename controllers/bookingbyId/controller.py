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

# Importación con fallback para BOOKING_SUCCESSFULLY_DELETED
try:
    from utils.message_codes import BOOKING_SUCCESSFULLY_DELETED
except ImportError:
    logging.warning("BOOKING_SUCCESSFULLY_DELETED not defined in utils.message_codes, using fallback")
    BOOKING_SUCCESSFULLY_DELETED = "BOOKING_SUCCESSFULLY_DELETED"

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
        data = [convert_to_serializable(item) for item in value]
    return data

class BookingByIdController(Resource):
    route = "/booking/<string:id>"

    @auth_required(permission='read', with_args=True)
    def get(self, id, **kwargs):
        if kwargs.get('current_user'):
            print(f"Current user: {kwargs}")
        else:
            print("No user data available")
        
        try:
            result = BookingModel.get_by_id(id)
            if result:
                result = convert_to_serializable(result)
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
            logging.error(f"Error getting booking by id: {ex}", exc_info=True)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    @auth_required(permission='write', with_args=True)
    def delete(self, id, **kwargs):
        if kwargs.get('current_user'):
            print(f"Current user: {kwargs}")
        else:
            print("No user data available")
        
        try:
            # Check if the booking exists
            booking = BookingModel.get_by_id(id)
            if not booking:
                return ServerResponse(
                    data={},
                    message="Booking does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

            # Attempt to delete the booking
            if not BookingModel.delete_by_id(id):
                logging.error(f"Failed to delete booking with id {id}: No document was deleted")
                return ServerResponse(
                    data={},
                    message="Booking does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

            return ServerResponse(
                data={},
                message="Booking successfully deleted",
                message_code=BOOKING_SUCCESSFULLY_DELETED,
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
            logging.error(f"Error deleting booking by id: {ex}", exc_info=True)
            return ServerResponse(
                data={},
                message=f"Error deleting booking: {str(ex)}",
                message_code="INTERNAL_SERVER_ERROR_MSG",
                status=StatusCode.INTERNAL_SERVER_ERROR
            )