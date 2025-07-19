from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.booking.model import BookingModel
import logging
import re
from utils.auth_manager import auth_required
from datetime import datetime
import pytz
from flask import jsonify

class BookingController(Resource):
    route = "/booking"

    """
    Create a new booking 
    """
    @auth_required(permission='write', with_args=True)
    def post(self,**kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            data = request.get_json()
            if not data.get("professor"):
                return ServerResponse(
                    message='professor is required', 
                    message_code=BOOKING_PROFESSOR_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )

            professor_email = data.get("professor_email")
            if not professor_email:
                return ServerResponse(
                    message='professor_email is required', 
                    message_code=BOOKING_PROFESSOR_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )
            
            if not re.match(r"^[\w\.-]+@utn\.ac\.cr$", professor_email):
                return ServerResponse(
                    message="Invalid email domain",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.BAD_REQUEST,
                )
            
            if not data.get("career"):
                return ServerResponse(
                    message='career is required', 
                    message_code=BOOKING_CAREER_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )
        
            if not data.get("subject"):
                return ServerResponse(
                    message='subject is required', 
                    message_code=BOOKING_SUBJECT_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )
            
            if not data.get("lab"):
                return ServerResponse(
                    message='lab is required', 
                    message_code=BOOKING_LAB_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )
            
            if not data.get("end_time"):
                return ServerResponse(
                    message='end_time is required', 
                    message_code=BOOKING_END_TIME_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )
            
            if not data.get("start_time"):
                return ServerResponse(
                    message='start_time is required', 
                    message_code=BOOKING_START_TIME_REQUIRED, 
                    status=StatusCode.BAD_REQUEST,
                )
            
            booking = BookingModel.create(data)
            return ServerResponse(booking.to_json(), message="Booking successfully created", 
                                  message_code=BOOKING_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
    """
    Get all booking labs filtered by current system dateTime
    """
    @auth_required(permission='read', with_args=True)
    def get(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")
        try:
            now = datetime.now()
            bookings = BookingModel.get_all_filtered_by_end_time(now)
            if not bookings:
                return jsonify(
                    data=[],
                    message="No bookings found that match the criteria",
                    message_code=BOOKING_NO_MATCHING_BOOKINGS
                )
            
            return ServerResponse(data=bookings, message="Bookings successfully retrieved",message_code=BOOKING_SUCCESSFULLY_RETRIEVED)
            
        except Exception as ex:
            logging.exception(ex)
            return jsonify(status=StatusCode.INTERNAL_SERVER_ERROR)