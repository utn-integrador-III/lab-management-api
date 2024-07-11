from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.booking.model import BookingModel
import logging
import re

class BookingController(Resource):
    route = "/book"

    """
    Create a new booking 
    """
    def post(self):
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
