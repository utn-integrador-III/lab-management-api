from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.booking.model import BookingModel
from datetime import datetime, timedelta
import logging
from utils.auth_manager import auth_required
from utils.message_codes import *
from bson import json_util
import json
class BookingByDateController(Resource):
    route = "/booking/date/<string:date>"

    @auth_required(permission='read', with_args=True)
    def get(self, date):
        try:
            filter_date = datetime.strptime(date, "%d-%m-%Y")
            start_of_day = datetime.combine(filter_date, datetime.min.time())
            end_of_day = start_of_day + timedelta(days=1)

            # Fetch bookings by start_time
            query = {
                "start_time": {
                    "$gte": start_of_day,
                    "$lt": end_of_day
                }
            }
            bookings = BookingModel.get_by_query(query)
            
            if bookings:
                serializable_bookings = json.loads(json_util.dumps(bookings))
                for booking in serializable_bookings:
                    booking.pop('_id', None)
                
                return ServerResponse(
                    data=serializable_bookings,
                    message="Bookings found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data=None,
                    message="No bookings found for the given date",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except ValueError:
            return ServerResponse(
                data=None,
                message="Invalid date format. Please use dd-mm-yyyy.",
                message_code=INVALID_DATE,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.error(f"Error getting bookings by date: {ex}")
            return ServerResponse(
                data=None,
                message="An internal server error occurred",
                message_code=INTERNAL_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )