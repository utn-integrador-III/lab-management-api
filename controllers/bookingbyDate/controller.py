from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from models.booking.model import BookingModel
from datetime import datetime, timedelta
import logging
from utils.auth_manager import auth_required
from utils.message_codes import *

class BookingByDateController(Resource):
    route = "/booking/date/<string:date>"

    @auth_required(permission='read', with_args=True)
    def get(self, date):
        current_user = request.args.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")

        try:
            filter_date = datetime.strptime(date, "%d-%m-%Y")
            start_of_day = datetime.combine(filter_date, datetime.min.time())
            end_of_day = start_of_day + timedelta(days=1)

            # Fetch bookings by start_time
            bookings = BookingModel.get_by_query({
                "start_time": {
                    "$gte": start_of_day,
                    "$lt": end_of_day
                }
            })

            if bookings:
                bookings = [booking.to_json() for booking in bookings]
                return ServerResponse(
                    data=bookings,
                    message="Bookings found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="No bookings found for the given date",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except ValueError:
            return ServerResponse(
                data={},
                message="Invalid date format. Please use dd-mm-yyyy.",
                message_code=INVALID_DATE,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.error(f"Error getting bookings by date: {ex}")
            return ServerResponse(
                status=StatusCode.INTERNAL_SERVER_ERROR
            )
        
    @staticmethod
    def get(current_user=None, date=None):
        try:
            if not date:
                raise ValueError("Date parameter is required.")
            
            # Parse the date string to a datetime object
            date_obj = datetime.strptime(date, '%d-%m-%Y')
            next_day = date_obj + timedelta(days=1)
            
            query = {
                'start_time': {
                    '$gte': date_obj,
                    '$lt': next_day
                }
            }
            
            bookings = BookingModel.get_by_query(query)
            
            # Convert datetime fields to strings
            bookings_data = [{
                'id': booking.id,
                'start_time': booking.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': booking.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                # Include other fields as needed
            } for booking in bookings]
            
            return {
                'data': bookings_data,
                'message': 'BOOKINGS_FOUND',
                'message_code': 'OK_MSG'
            }
        except Exception as ex:
            logging.error(f"Error processing request: {ex}")
            return {
                'message': f"Error processing request: {str(ex)}",
                'message_code': 'ERROR_MSG'
            }, 500
