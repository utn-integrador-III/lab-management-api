
import traceback


from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *

from models.lab.model import LabModel
import logging
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

# Helper function to convert MongoDB ObjectId and datetime objects to serializable formats
def convert_object(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [convert_object(item) for item in obj]
    if isinstance(obj, dict):
        return {key: convert_object(value) for key, value in obj.items()}
    return obj

class BookingController(Resource):
    route = "/booking"

    def put(self):
       
        try:
            # Parse and log the incoming JSON data from the request body
            update_data = request.get_json()
            logging.info(f"Received update data: {update_data}")

            # Validate that the incoming data is a dictionary
            if not update_data or not isinstance(update_data, dict):
                return ServerResponse(
                    message="No valid data provided for update",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Extract and validate the lab_book_id from the incoming data
            lab_book_id = update_data.get("lab_book_id")
            if not lab_book_id:
                return ServerResponse(
                    message="Lab book ID is required",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            logging.info(f"Attempting to retrieve lab book with ID: {lab_book_id}")

            # Attempt to retrieve the lab book from the database
            try:
                lab_book = LabModel.get_by_id(lab_book_id)
                logging.info(f"Retrieved lab book: {lab_book}")
            except Exception as ex:
                logging.error(f"Error retrieving lab book: {ex}")
                logging.error(traceback.format_exc())
                return ServerResponse(
                    message=f"Error retrieving lab book: {str(ex)}",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            # Validate that the lab book was found
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
                update_success = LabModel.update(lab_book_id, {"students": lab_book["students"]})
                logging.info(f"Update result: {update_success}")
            except Exception as ex:
                logging.error(f"Error updating lab book: {ex}")
                logging.error(traceback.format_exc())
                return ServerResponse(
                    message=f"Error updating lab book: {str(ex)}",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            # Validate the update success
            if not update_success:
                return ServerResponse(
                    message="Failed to book computer",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            # Convert the lab book object to a serializable format
            lab_book = convert_object(lab_book)

            # Return a successful response with the updated lab book data
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
=======
from models.booking.model import BookingModel
import logging

class BookingController(Resource):
    route = "/booking/computer"

    def delete(self):
        try:
            # Obtener datos del cuerpo de la solicitud
            data = request.get_json()
            logging.info(f"Datos recibidos: {data}")

            lab_id = data.get('id')
            student_email = data.get('student_email')
            computer = data.get('computer')

            logging.info(f"ID del laboratorio: {lab_id}, Email del estudiante: {student_email}, Computadora: {computer}")

            # Verificar que todos los datos necesarios estén presentes
            if not lab_id or not student_email or not computer:
                logging.warning("Faltan datos requeridos")
                return ServerResponse(
                    message='Faltan datos requeridos', 
                    message_code=INCORRECT_REQUEST_PARAM, 
                    status=StatusCode.BAD_REQUEST
                )

            # Eliminar la reserva
            success, message = BookingModel.delete_reservation(lab_id, student_email, computer)

            if success:
                logging.info("Reserva eliminada exitosamente")
                return ServerResponse(
                    message=message, 
                    message_code=SUCCESS_MSG,
                    status=StatusCode.OK
                )
            else:
                logging.error(f"Error al eliminar la reserva: {message}")
                return ServerResponse(
                    message=message, 
                    message_code=ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            logging.exception(e)
            return ServerResponse(
                message=str(e), 
                message_code=ERROR_MSG,
                status=StatusCode.INTERNAL_SERVER_ERROR

            )
