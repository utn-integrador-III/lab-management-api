from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.booking.model import BookingModel
import logging

class BookingComputerController(Resource):
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
