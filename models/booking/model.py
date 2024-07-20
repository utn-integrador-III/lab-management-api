from datetime import datetime
from bson import ObjectId
from flask import config as flask_config
import pytz
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.booking.db_queries import __dbmanager__, find_by_id, update
import logging
from pymongo.errors import ServerSelectionTimeoutError

class BookingModel:
    def __init__(self, professor=None, professor_email=None, career=None, subject=None, lab=None, end_time=None, start_time=None, students=None, observations=None):
        self.professor = professor
        self.professor_email = professor_email
        self.career = career if career else {}
        self.subject = subject if subject else {}
        self.lab = lab
        self.end_time = end_time
        self.start_time = start_time
        self.students = students if students else []
        self.observations = observations

    def to_dict(self):
        return {
            "professor": self.professor,
            "professor_email": self.professor_email,
            "career": self.career,
            "subject": self.subject,
            "lab": self.lab,
            "end_time": self.end_time,
            "start_time": self.start_time,
            "students": self.students,
            "observations": self.observations,
        }

    def to_json(self):
        return {
            "professor": self.professor,
            "professor_email": self.professor_email,
            "career": self.career,
            "subject": self.subject,
            "lab": self.lab,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "students": self.students,
            "observations": self.observations,
        }

    @classmethod
    def create(cls, data):
        try:
            if "end_time" in data and isinstance(data["end_time"], str):
                data["end_time"] = cls._parse_datetime(data["end_time"])
            if "start_time" in data and isinstance(data["start_time"], str):
                data["start_time"] = cls._parse_datetime(data["start_time"])

            booking = BookingModel(**data)
            __dbmanager__.create_data(booking.to_dict())
            return booking
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create booking: " + str(ex))

    @staticmethod
    def _parse_datetime(date_str):
        # Parse the string to a datetime object
        parsed_datetime = datetime.fromisoformat(date_str)
        costa_rica_tz = pytz.timezone('America/Costa_Rica')

        # If the datetime is naive, localize it; otherwise, convert it to the desired time zone
        if parsed_datetime.tzinfo is None:
            localized_datetime = costa_rica_tz.localize(parsed_datetime)
        else:
            localized_datetime = parsed_datetime.astimezone(costa_rica_tz)
        
        return localized_datetime
    
    @staticmethod
    def delete_reservation(lab_id, student_email, computer):
        try:
            lab = find_by_id(lab_id)
            if not lab:
                logging.error("Laboratorio no encontrado")
                return False, 'Laboratorio no encontrado'

            logging.info(f"Estudiantes antes de eliminar la reserva: {lab['students']}")

            for student in lab['students']:
                logging.info(f"Procesando estudiante: {student}")
                if student['student_email'] == student_email and student['computer'] == computer:
                    logging.info(f"Reserva encontrada: {student}")

            new_students = [s for s in lab['students'] if not (s['student_email'] == student_email and s['computer'] == computer)]
            logging.info(f"Estudiantes después de eliminar la reserva: {new_students}")

            if len(new_students) == len(lab['students']):
                logging.error("Reserva no encontrada")
                return False, 'Reserva no encontrada'

            lab['students'] = new_students
            updated = update(lab_id, lab)
            if updated:
                logging.info("Reserva eliminada exitosamente")
                return True, 'Reserva eliminada exitosamente'
            else:
                logging.error("Error al eliminar la reserva")
                return False, 'Error al eliminar la reserva'
        except Exception as e:
            logging.exception(e)
            return False, str(e)
        
    @staticmethod
    def find_by_id(lab_book_id):
        try:
            return __dbmanager__.get_by_id(lab_book_id)
        except ServerSelectionTimeoutError as e:
            logging.error(f"Database connection error: {e}")
            raise   
    @staticmethod
    def update(lab_book_id, update_data):
        return __dbmanager__.update_data(lab_book_id, update_data)