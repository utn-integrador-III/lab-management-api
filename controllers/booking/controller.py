
import datetime
import traceback
from flask_restful import Resource
from flask import config, request
from utils.server_response import *
from utils.message_codes import *
from models.booking.model import BookingModel
import logging
import re
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError



def convert_object(obj):
    if isinstance(obj, list):
        return [convert_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_object(value) for key, value in obj.items()}
    elif isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj


class BookingController(Resource):
    route = "/booking"

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

    def put(self):
        try:
            update_data = request.get_json()
            logging.info(f"Received update data: {update_data}")

            if not update_data or not isinstance(update_data, dict):
                return ServerResponse(
                    message="No valid data provided for update",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            lab_book_id = update_data.get("lab_book_id")
            if not lab_book_id:
                return ServerResponse(
                    message="Lab book ID is required",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            logging.info(f"Attempting to retrieve lab book with ID: {lab_book_id}")

            try:
                lab_book = BookingModel.find_by_id(lab_book_id)
                logging.info(f"Retrieved lab book: {lab_book}")
            except ServerSelectionTimeoutError as ex:
                logging.error(f"Database connection error: {ex}")
                return ServerResponse(
                    message="Unable to connect to the database. Please try again later.",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )
            except Exception as ex:
                logging.error(f"Error retrieving lab book: {ex}")
                logging.error(traceback.format_exc())
                return ServerResponse(
                    message=f"Error retrieving lab book: {str(ex)}",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not lab_book:
                return ServerResponse(
                    message="Lab book not found",
                    message_code=LAB_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                )

            # Ensure the 'students' attribute exists in the lab book and initialize if necessary
            if "students" not in lab_book:
                lab_book["students"] = []

            # Check if the computer is already booked by another student
            try:
                if any(student["computer"] == update_data["computer"] for student in lab_book["students"]):
                    return ServerResponse(
                        message="Computer already booked",
                        message_code=CONFLICT_MSG,
                        status=StatusCode.CONFLICT,
                    )
            except KeyError as ke:
                logging.error(f"KeyError when checking computer availability: {ke}")
                logging.error(traceback.format_exc())
                return ServerResponse(
                    message=f"Invalid update data: missing key {str(ke)}",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Create the new student entry from the incoming data
            try:
                new_student = {
                    "student_email": update_data["student_email"],
                    "student_name": update_data["student_name"],
                    "computer": update_data["computer"],
                    "usage_time": update_data["usage_time"]
                }
            except KeyError as ke:
                logging.error(f"KeyError when creating new student: {ke}")
                logging.error(traceback.format_exc())
                return ServerResponse(
                    message=f"Invalid update data: missing key {str(ke)}",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Add the new student to the lab book's student list
            lab_book["students"].append(new_student)

            # Update the lab book in the database
            try:
                update_success = BookingModel.update(lab_book_id, {"students": lab_book["students"]})
                logging.info(f"Update result: {update_success}")
            except ServerSelectionTimeoutError as ex:
                logging.error(f"Database connection error during update: {ex}")
                return ServerResponse(
                    message="Unable to connect to the database. Please try again later.",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )
            except Exception as ex:
                logging.error(f"Error updating lab book: {ex}")
                logging.error(traceback.format_exc())
                return ServerResponse(
                    message=f"Error updating lab book: {str(ex)}",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not update_success:
                return ServerResponse(
                    message="Failed to book computer",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            # Convert the lab book object to a serializable format
            lab_book = convert_object(lab_book)

            return ServerResponse(
                data=lab_book,
                message="Computer booked successfully",
                message_code=LAB_SUCCESSFULLY_UPDATED,
                status=StatusCode.OK,
            )

        except Exception as ex:
            logging.error(f"Unexpected error: {ex}")
            logging.error(traceback.format_exc())
            return ServerResponse(
                message=f"An unexpected error occurred: {str(ex)}",
                message_code=INTERNAL_SERVER_ERROR_MSG,
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )